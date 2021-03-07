import json
import logging
from pathlib import Path

from spotipy import Spotify as Client
from spotipy.oauth2 import SpotifyClientCredentials

import dotify.models as models


class Dotify:
    SCHEMA_DIR = Path(__file__).parent / 'models' / 'schema'

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

    def _construct_view(self, view_name):
        base = getattr(models, view_name)

        return type(view_name, (base,), {
            'client': self
        })

    @property
    def Track(self):
        return self._construct_view('Track')

    @property
    def Album(self):
        return self._construct_view('Album')

    @property
    def Playlist(self):
        return self._construct_view('Playlist')

    def search(self, query, type, limit=1):
        results = self.client.search(query, type=type, limit=limit)

        if len(results[f'{type}s']['items']) == 0:
            raise self.NotFound

        return results[f'{type}s']['items']
