import logging
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from api.api import api
from api.error.errors import BadRequest, InternalServerError, NotFound
from flask import request, send_file
from api.provider import DEFAULT, Spotify, SpotifyAlbumNotFoundError


@api.route("/playlist", methods=['POST', ])
def playlist():
    data = request.json

    if data is None or 'uri' not in data:
        raise BadRequest('No playlist uri')

    try:
        with tempfile.TemporaryDirectory() as tmp:
            with Spotify(output_file=f'{Path(tmp) / DEFAULT["output_file"]}') as spotify:
                metadata, uris = spotify.fetch_playlist(data['uri'])

                name = metadata["name"]

                paths = []
                for i, (path, metadata) in enumerate(spotify.download_tracks(uris)):
                    if path is not None:
                        paths.append(path)
                    else:
                        logging.warning(f'Failed to download track {uris[i]}')

                attachment_filename = f"{name}.zip"

                path = Path(tmp) / attachment_filename

                logging.info(f'Zipping playlist {data["uri"]} to {path}')

                zipfile = ZipFile(path, 'w', ZIP_DEFLATED)
                for path in paths:
                    zipfile.write(path, Path(path).name)

                logging.info(f'Sending zip file {attachment_filename}')

                return send_file(path, as_attachment=True, attachment_filename=attachment_filename)
    except SpotifyAlbumNotFoundError:
        raise NotFound(f'No playlist corresponding to {data["uri"]}')
    except Exception as e:
        logging.exception(e)
        raise InternalServerError(str(e))
