import logging
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from flask import Flask, abort, jsonify, request, send_file
from spotify import (SPOTIFY, Spotify, SpotifyAlbumNotFoundError,
                     SpotifyException)

app = Flask("Spotify Downloader API")


@app.route("/track", methods=['POST', ])
def track():
    data = request.json

    if data is None or 'uri' not in data:
        abort(400)

    try:
        with Spotify(SPOTIFY) as spotify:
            path, metadata = spotify.download_track(data['uri'])

            artist, name = metadata["artist"]["name"], metadata["name"]

            attachment_filename = f"{artist} - {name}.mp3"

            return send_file(path, as_attachment=True, attachment_filename=attachment_filename)
    except SpotifyException:
        abort(404)
    except Exception as e:
        logging.exception(e)
        abort(500)


@app.route("/album", methods=['POST', ])
def album():
    data = request.json

    if data is None or 'uri' not in data:
        abort(400)

    try:
        with Spotify(SPOTIFY) as spotify:
            metadata, uris = spotify.fetch_album(data['uri'])

            artist, name = metadata["artist"]["name"], metadata["name"]

            paths = []
            for path, metadata in spotify.download_tracks(uris):
                if path is not None:
                    paths.append(path)

        with tempfile.TemporaryDirectory() as tmp:
            attachment_filename = f"{artist} - {name}.zip"

            path = Path(tmp) / attachment_filename

            zipfile = ZipFile(path, 'w', ZIP_DEFLATED)
            for path in paths:
                zipfile.write(path, Path(path).name)

            return send_file(path, as_attachment=True, attachment_filename=attachment_filename)
    except SpotifyAlbumNotFoundError:
        abort(404)
    except Exception as e:
        logging.exception(e)
        abort(500)


if __name__ == "__main__":
    app.run()
