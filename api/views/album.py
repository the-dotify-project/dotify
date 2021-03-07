import logging
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from api.api import api
from api.error.errors import BadRequest, InternalServerError, NotFound
from api.settings import DOTIFY_SETTINGS
from flask import request, send_file
from dotify import Dotify, Album

ID, SECRET = DOTIFY_SETTINGS['spotify_id'], DOTIFY_SETTINGS['spotify_secret']


@api.route("/album/download", methods=['POST', ])
def album():
    data = request.json

    if data is None or 'url' not in data:
        raise BadRequest('No album url')

    url = data['url']

    try:
        with tempfile.TemporaryDirectory() as tmp:
            with Dotify(ID, SECRET) as spotify:
                album = Album.from_url(spotify, url)

                artist, name = album.artist.name, album.name

                filename = f'{artist} - {name}'
                path = Path(tmp) / filename

                album.download(path)

                attachment_filename = f"{filename}.zip"
                attachment_path = Path(tmp) / attachment_filename

                logging.info(f'Zipping album {url} to {path}')

                zipfile = ZipFile(attachment_path, 'w', ZIP_DEFLATED)
                for entry in path.iterdir():
                    if entry.is_file():
                        zipfile.write(entry, entry.name)

                logging.info(f'Sending zip file {attachment_filename}')

                return send_file(path, as_attachment=True, attachment_filename=attachment_filename)
    except Album.NotFound:
        raise NotFound(f'No album corresponding to {url}')
    except Album.InvalidURL:
        raise BadRequest(f'{url} is not a valid Dotify album URL')
    except Exception as e:
        logging.exception(e)
        raise InternalServerError(str(e))
