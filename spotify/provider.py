import logging

from spotipy import Spotify as Client
from spotipy.oauth2 import SpotifyClientCredentials

import spotify.models as models


class Spotify:
    URL = 'https://open.spotify.com/'

    class GeneralException(Exception):
        pass

    class NoSearchResults(GeneralException):
        pass

    def __init__(self, client_id, client_secret):
        self.logger = logging.getLogger(self.__class__.__name__)

        self.credential_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )

    def __del__(self):
        if self.is_connected is True:
            self.disconnect()

    def __enter__(self):
        self.connect()

        return self

    def __exit__(self, exc_type, exc_value, exc_trace):
        self.disconnect()

        if exc_type is not None:
            self.logger.exception(f'{exc_type.__name__}: {exc_value}')

    def connect(self):
        if self.is_connected is False:
            self.client = Client(
                client_credentials_manager=self.credential_manager
            )

    def disconnect(self):
        if self.is_connected is True:
            del self.client

    @property
    def is_connected(self):
        return hasattr(self, 'client')

    def search(self, query, limit=10, about='track'):
        results = self.client.search(query, type=about, limit=limit)

        if len(results[f'{about}s']['items']) == 0:
            raise Spotify.NoSearchResults

        return results[f'{about}s']['items']

    def search_track(self, query, limit=10):
        return models.Track.search(self, query, limit=limit)

    def search_album(self, query, limit=10):
        return models.Album.search(self, query, limit=limit)

    def search_playlist(self, query, limit=10):
        return models.Playlist.search(self, query, limit=limit)

    def track_from_url(self, url):
        return models.Track.from_url(self, url)

    def album_from_url(self, url):
        return models.Album.from_url(self, url)

    def playlist_from_url(self, url):
        return models.Playlist.from_url(self, url)
