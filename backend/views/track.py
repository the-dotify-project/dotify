import logging
import tempfile
from pathlib import Path

from flask import abort, request, send_file
from spotify import DEFAULT, Spotify, SpotifyException

from backend.api import api


@api.route("/track", methods=['POST', ])
def track():
    data = request.json

    if data is None or 'uri' not in data:
        abort(400)

    try:
        with tempfile.TemporaryDirectory() as tmp:
            with Spotify(output_file=f'{Path(tmp) / DEFAULT["output_file"]}') as spotify:
                path, metadata = spotify.download_track(data['uri'])

                artist, name = metadata["artist"]["name"], metadata["name"]

                attachment_filename = f"{artist} - {name}.mp3"

                logging.info(f'Sending MP3 file {attachment_filename}')

                return send_file(path, as_attachment=True, attachment_filename=attachment_filename)
    except SpotifyException:
        abort(404)
    except Exception as e:
        logging.exception(e)
        abort(500, str(e))
