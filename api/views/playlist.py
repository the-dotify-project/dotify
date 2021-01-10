import logging
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from api.api import api
from api.error.errors import BadRequest, InternalServerError, NotFound
from api.settings import DOTIFY_SETTINGS
from flask import request, send_file
from spotify import Spotify, Playlist

ID, SECRET = DOTIFY_SETTINGS['spotify_id'], DOTIFY_SETTINGS['spotify_secret']


@api.route("/playlist/download", methods=['POST', ])
def playlist():
    data = request.json

    if data is None or 'url' not in data:
        raise BadRequest('No playlist url')

    url = data['url']

    try:
        with tempfile.TemporaryDirectory() as tmp:
            with Spotify(ID, SECRET) as spotify:
                playlist = Playlist.from_url(spotify, url)

                filename = playlist.name
                path = Path(tmp) / filename

                playlist.download(path)

                attachment_filename = f"{filename}.zip"
                attachment_path = Path(tmp) / attachment_filename

                logging.info(f'Zipping playlist {url} to {path}')

                zipfile = ZipFile(attachment_path, 'w', ZIP_DEFLATED)
                for entry in path.iterdir():
                    if entry.is_file():
                        zipfile.write(entry, entry.name)

                logging.info(f'Sending zip file {attachment_filename}')

                return send_file(path, as_attachment=True, attachment_filename=attachment_filename)
    except Playlist.NotFound:
        raise NotFound(f'No playlist corresponding to {url}')
    except Playlist.InvalidURL:
        raise BadRequest(f'{url} is not a valid Spotify playlist URL')
    except Exception as e:
        logging.exception(e)
        raise InternalServerError(str(e))
