import logging
from functools import wraps

from spotipy import Spotify as Client
from spotipy.client import logger
from spotipy.oauth2 import SpotifyClientCredentials

import dotify.models as models


class Dotify(Client):
    def __init__(self, client_id, client_secret):
        super().__init__(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=client_id,
                client_secret=client_secret
            )
        )

        class_name = self.__class__.__name__
        self.logger = logging.getLogger(f'{logger.name}.{class_name}')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_trace):
        self._session.close()

        if exc_type is not None:
            self.logger.exception(f'{exc_type.__name__}: {exc_value}')

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

    def search(self, type, query, limit=1):
        results = super().search(query, type=type, limit=limit)

        return results[f'{type}s']['items']
