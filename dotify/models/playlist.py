from pathlib import Path

import dotify.models as models
from dotify.models.model import Model


class Playlist(Model):
    class Json:
        schema = Model.Json.schema_dir / 'playlist.json'

        @classmethod
        def dependencies(cls):
            return [models.User, models.Image]

    class InvalidURL(Model.InvalidURL):
        pass

    class NotFound(Model.NotFound):
        pass

    @property
    def url(self):
        return self.external_urls.spotify

    @property
    def tracks(self):
        response, offset = self.client.playlist_tracks(self.url), 0

        while True:
            for result in response['items']:
                url = result['track']['external_urls']['spotify']

                yield self.client.Track.from_url(url)

            offset += len(response['items'])

            if response['next'] is None:
                break

            response = self.client.playlist_tracks(self.url, offset=offset)

    def __str__(self):
        return self.name

    def download(self, path, skip_existing=False, logger=None):
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
        metadata = cls.client.playlist(url)

        if 'tracks' in metadata:
            del metadata['tracks']

        return cls(**metadata)
