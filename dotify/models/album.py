from pathlib import Path

import requests
from mutagen.id3 import APIC as AlbumCover

import dotify.models as models
from dotify.models.model import Model


class Album(Model):
    """ """
    class Json:
        """ """
        schema = Model.Json.schema_dir / 'album.json'

        @classmethod
        def dependencies(cls):
            """ """
            return [models.Track, models.Artist, models.Image]

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
        response, offset = self.client.album_tracks(self.url), 0

        while True:
            for result in response['items']:
                url = result['external_urls']['spotify']

                yield self.client.Track.from_url(url)

            offset += len(response['items'])

            if response['next'] is None:
                break

            response = self.client.client.album_tracks(self.url, offset=offset)

    def download(self, path, skip_existing=False, logger=None):
        """

        :param path: 
        :param skip_existing:  (Default value = False)
        :param logger:  (Default value = None)

        
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

        :param url: 

        
        """
        return cls(**cls.client.album(url))
