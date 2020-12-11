import logging
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from api.api import api
from api.error.errors import BadRequest, InternalServerError, NotFound
from api.settings import DOTIFY_SETTINGS
from flask import request, send_file
from spotify import Spotify

ID, SECRET = DOTIFY_SETTINGS['spotify_id'], DOTIFY_SETTINGS['spotify_secret']


@api.route("/album", methods=['POST', ])
def album():
    data = request.json

    if data is None or 'url' not in data:
        raise BadRequest('No album url')

    url = data['url']

    try:
        with tempfile.TemporaryDirectory() as tmp:
            with Spotify(ID, SECRET) as spotify:
                tracks = spotify.tracks_of_album(url)

                metadata, uris = spotify.fetch_album(url)

                artist, name = metadata["artist"]["name"], metadata["name"]

                paths = []
                for i, (path, metadata) in enumerate(spotify.download_tracks(uris)):
                    if path is not None:
                        paths.append(path)
                    else:
                        logging.warning(f'Failed to download track {uris[i]}')

                attachment_filename = f"{artist} - {name}.zip"

                path = Path(tmp) / attachment_filename

                logging.info(f'Zipping album {url} to {path}')

                zipfile = ZipFile(path, 'w', ZIP_DEFLATED)
                for path in paths:
                    zipfile.write(path, Path(path).name)

                logging.info(f'Sending zip file {attachment_filename}')

                return send_file(path, as_attachment=True, attachment_filename=attachment_filename)
    except SpotifyAlbumNotFoundError:
        raise NotFound(f'No album corresponding to {url}')
    except Exception as e:
        logging.exception(e)
        raise InternalServerError(str(e))
