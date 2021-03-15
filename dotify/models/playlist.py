import html
from pathlib import Path

import dotify.models.base as base
import dotify.models as models


class Playlist(base.Base):
    class InvalidURL(base.Base.InvalidURL):
        pass

    class NotFound(base.Base.NotFound):
        pass

    def __init__(self, metadata, tracks):
        self.metadata = metadata
        self.tracks = tracks

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Playlist "{self.name}">'

    @staticmethod
    def extract_metadata(metadata):
        return {
            'url': metadata["external_urls"]["spotify"],
            'name': html.unescape(metadata['name']).strip(),
            'description': html.unescape(metadata['description']).strip(),
            'images': metadata['images']
        }

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

    @property
    def name(self):
        return self.metadata['name']

    @property
    def url(self):
        return self.metadata['url']

    @property
    def description(self):
        return self.metadata['description']

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
