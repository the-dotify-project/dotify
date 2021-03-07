from pathlib import Path

from dotify.models.artist import Artist
from dotify.models.base import Base
from dotify.models.image import Image
from dotify.models.track import Track


class Album(Base):
    schema = Path(__file__).parent / 'schema' / 'album.json'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # TODO: Initialize tracks (or NOT ?)

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
    def from_url(cls, spotify, url):
        cls.assert_valid_url(url)

        metadata = cls.extract_metadata(spotify.client.album(url))

        results = spotify.client.album_tracks(url)

        tracks = []
        while True:
            for result in results['items']:
                url = result['external_urls']['spotify']
                tracks.append(Track.from_url(spotify, url))

            if not results['next']:
                break

            results = spotify.client.album_tracks(url, offset=len(tracks))

        return cls(metadata, tracks)

    def download(self, path):
        path = Path(path)

        path.mkdir(parents=True, exist_ok=True)

        for track in self.tracks:
            # FIXME: convert to `Artist`
            artist = track.artists[0]
            name = track.name

            track.download(path / f'{artist} - {name}.mp3')
