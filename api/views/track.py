import logging
import tempfile
from pathlib import Path

from api.api import api
from api.error.errors import BadRequest, InternalServerError, NotFound
from api.settings import DOTIFY_SETTINGS
from flask import request, send_file
from spotify import Spotify, Track

ID, SECRET = DOTIFY_SETTINGS['spotify_id'], DOTIFY_SETTINGS['spotify_secret']


@api.route("/track/download", methods=['POST', ])
def track():
    data = request.json

    if data is None or 'url' not in data:
        raise BadRequest('No track url')

    url = data['url']

    try:
        with tempfile.TemporaryDirectory() as tmp:
            with Spotify(ID, SECRET) as spotify:
                track = Track.from_url(spotify, url)

                artist = track.artists[0]
                name = track.name

                path = Path(tmp) / f'{artist} - {name}.mp3'

                track.download(path)

                attachment_filename = f"{artist} - {name}.mp3"

                logging.info(f'Sending MP3 file {attachment_filename}')

                return send_file(path, as_attachment=True, attachment_filename=attachment_filename)
    except Track.NotFound:
        raise NotFound(f'No track corresponding to {url}')
    except Track.InvalidURL:
        raise BadRequest(f'{url} is not a valid Spotify track URL')
    except Exception as e:
        logging.exception(e)
        raise InternalServerError(str(e))
