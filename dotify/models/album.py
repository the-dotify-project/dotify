import logging
from pathlib import Path

import dotify.models as models
import requests

from dotify.dotify import Dotify
from dotify.model import Model, logger
from mutagen.id3 import APIC as AlbumCover

logger = logging.getLogger(f'{logger.name}.{__name__}')


class Album(Model):
    """ """
    class Json:
        """ """
        dependencies = [
            'dotify.models.Track',
            'dotify.models.Artist',
            'dotify.models.Image'
        ]

    def __str__(self):
        return f'{self.artist} - {self.name}'

    @property
    def artist(self):
        """ """
        return self.artists[0]

    @property
    def url(self):
        """ """
        return self.external_urls.spotify

    @property
    def cover(self):
        """ """
        response = requests.get(self.images[0].url)

        assert response.status_code == 200, f"Failed to fetch {self.images[0].url}"

        return AlbumCover(
            encoding=3,
            mime='image/jpeg',
            type=3,
            desc='Cover',
            data=response.content
        )

    @property
    def tracks(self):
        """ """
        response, offset = self.context.album_tracks(self.url), 0

        while True:
            for result in response['items']:
                url = result['external_urls']['spotify']

                yield models.Track.from_url(url)

            offset += len(response['items'])

            if response['next'] is None:
                break

            response = cls.context.album_tracks(self.url, offset=offset)

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
        return cls(**cls.context.album(url))
