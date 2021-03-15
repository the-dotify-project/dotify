from pathlib import Path

import dotify.models.base as base
import dotify.models as models


class Album(base.Base):
    class Json:
        schema = base.Base.Json.schema_dir / 'album.json'

        @classmethod
        def dependencies(cls):
            return [models.Track, models.Artist, models.Image]

    @property
    def artist(self):
        return self.artists[0]

    @property
    def url(self):
        return self.external_urls.spotify

    def __str__(self):
        return f'{self.artist} - {self.name}'

    def __repr__(self):
        return f'<Album "{str(self)}">'

    @classmethod
    def from_url(cls, url):
        cls.assert_valid_url(url)

        metadata = cls.extract_metadata(self.client.client.album(url))

        results = self.client.client.album_tracks(url)

        tracks = []
        while True:
            for result in results['items']:
                url = result['external_urls']['spotify']
                tracks.append(self.client.Track.from_url(url))

            if not results['next']:
                break

            results = self.client.client.album_tracks(url, offset=len(tracks))

        return cls(metadata, tracks)

    def download(self, path):
        path = Path(path)

        path.mkdir(parents=True, exist_ok=True)

        for track in self.tracks:
            # FIXME: convert to `Artist`
            artist = track.artists[0]
            name = track.name

            track.download(path / f'{artist} - {name}.mp3')
