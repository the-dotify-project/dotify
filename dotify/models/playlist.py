import logging
from pathlib import Path

import dotify.models as models
from dotify.dotify import Dotify
from dotify.model import Model, logger

logger = logging.getLogger(f'{logger.name}.{__name__}')


class Playlist(Model):
    """ """
    class Json:
        """ """
        schema = 'playlist.json'

        @classmethod
        def dependencies(cls):
            """ """
            return [models.User, models.Image]

    def __init__(self, **props):
        if 'tracks' in props:
            del props['tracks']

        super().__init__(**props)

    def __str__(self):
        return self.name

    @property
    def url(self):
        """ """
        return self.external_urls.spotify

    @property
    def tracks(self):
        """ """
        response, offset = Dotify.get_context().playlist_tracks(self.url), 0

        while True:
            for result in response['items']:
                url = result['track']['external_urls']['spotify']

                yield models.Track.from_url(url)

            offset += len(response['items'])

            if response['next'] is None:
                break

            response = Dotify.get_context().playlist_tracks(self.url, offset=offset)

    def download(self, path, skip_existing=False, logger=None):
        """






        """
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)

        for track in self.tracks:
            track.download(
                path / f'{track}.mp3',
                skip_existing=skip_existing, logger=logger
            )

        return path

    @classmethod
    @Model.validate_url
    @Model.convert_to_model_error
    def from_url(cls, url):
        """




        """
        return cls(**Dotify.get_context().playlist(url))
