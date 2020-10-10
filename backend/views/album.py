
import logging
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from backend.api import api
from flask import abort, request, send_file
from spotify import DEFAULT, Spotify, SpotifyAlbumNotFoundError


@api.route("/album", methods=['POST', ])
def album():
    data = request.json

    if data is None or 'uri' not in data:
        abort(400)

    try:
        with tempfile.TemporaryDirectory() as tmp:
            with Spotify(output_file=f'{Path(tmp) / DEFAULT["output_file"]}') as spotify:
                metadata, uris = spotify.fetch_album(data['uri'])

                artist, name = metadata["artist"]["name"], metadata["name"]

                paths = []
                for i, (path, metadata) in enumerate(spotify.download_tracks(uris)):
                    if path is not None:
                        paths.append(path)
                    else:
                        logging.warning(f'Failed to download track {uris[i]}')

                attachment_filename = f"{artist} - {name}.zip"

                path = Path(tmp) / attachment_filename

                logging.info(f'Zipping album {data["uri"]} to {path}')

                zipfile = ZipFile(path, 'w', ZIP_DEFLATED)
                for path in paths:
                    zipfile.write(path, Path(path).name)

                logging.info(f'Sending zip file {attachment_filename}')

                return send_file(path, as_attachment=True, attachment_filename=attachment_filename)
    except SpotifyAlbumNotFoundError:
        abort(404)
    except Exception as e:
        logging.exception(e)
        abort(500, str(e))
