import html
from pathlib import Path

from spotify.models.artist import Artist
from spotify.models.image import Image
from spotify.models.track import Track
from spotify.provider import Spotify
from spotify.sanity import assert_valid_url


class Album:
    URL = f'{Spotify.URL}/album/'

    class InvalidURL(Spotify.GeneralException):
        pass

    def __init__(self, metadata, tracks):
        super().__init__()

        self.metadata = metadata
        self.tracks = tracks

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Album "{self.name}">'

    @staticmethod
    def extract_metadata(metadata):
        return {
            "url": metadata["external_urls"]["spotify"],
            "name": html.unescape(metadata["name"]),
            "artist": {
                "name": html.unescape(metadata["artists"][0]["name"]),
                "url": metadata["artists"][0]["external_urls"]["spotify"],
            },
            "images": metadata["images"]
        }

    @classmethod
    def assert_valid_url(cls, url):
        assert_valid_url(
            r"https?://open.spotify.com/album/.+",
            url,
            cls.InvalidURL(f'{url} is not a valid spotify album url')
        )

    @classmethod
    def search(cls, spotify, query, limit=10):
        return map(cls.extract_metadata, spotify.search(query, limit=limit, about='album'))

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

    @property
    def artist(self):
        return Artist(
            self.metadata['artist']['name'],
            self.metadata['artist']['url']
        )

    @property
    def images(self):
        return [
            Image(image['height'], image['width'], image['url'])
            for image in self.metadata['images']
        ]

    @property
    def name(self):
        return self.metadata['name']

    @property
    def url(self):
        return self.metadata['metadata']

    def download(self, path):
        path = Path(path)

        path.mkdir(parents=True, exist_ok=True)

        for track in self.tracks:
            # FIXME: convert to `Artist`
            artist = track.artists[0]
            name = track.name

            track.download(path / f'{artist} - {name}.mp3')
