from pathlib import Path

import dotify.models.base as base
import dotify.models as models


class Playlist(base.Base):
    class Json:
        schema = base.Base.Json.schema_dir / 'playlist.json'

        @classmethod
        def dependencies(cls):
            return [models.User, models.Image]

    class InvalidURL(base.Base.InvalidURL):
        pass

    class NotFound(base.Base.NotFound):
        pass

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Playlist "{str(self)}">'

    @classmethod
    def from_url(cls, spotify, url):
        cls.assert_valid_url(url)

        metadata = cls.extract_metadata(spotify.client.playlist(url))

        results = spotify.client.playlist_tracks(url)

        tracks = []
        while True:
            for result in results['items']:
                url = result['track']['external_urls']['spotify']
                # tracks.append(Track.from_url(spotify, url))

            if not results['next']:
                break

            results = spotify.client.playlist_tracks(url, offset=len(tracks))

        return cls(metadata, tracks)

    # @property
    # def name(self):
    #     return self.metadata['name']

    @property
    def url(self):
        return self.external_urls.spotify

    # @property
    # def description(self):
    #     return self.metadata['description']

    # @property
    # def images(self):
    #     return [
    #         Image(image['height'], image['width'], image['url'])
    #         for image in self.metadata['images']
    #     ]

    def download(self, path):
        path = Path(path)

        path.mkdir(parents=True, exist_ok=True)

        for track in self.tracks:
            artist = track.artists[0]  # ! convert to `Artist`
            name = track.name

            track.download(path / f'{artist} - {name}.mp3')
