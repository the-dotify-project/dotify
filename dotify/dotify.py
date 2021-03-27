import logging
import threading

from spotipy import Spotify as Client
from spotipy.client import logger
from spotipy.oauth2 import SpotifyClientCredentials

logger = logging.getLogger(f'{logger.name}.{__name__}')


class Dotify(Client):
    """ """
    __context = threading.local()

    def __init__(self, client_id, client_secret):
        super().__init__(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=client_id,
                client_secret=client_secret
            )
        )

    def __del__(self):
        if hasattr(self, '_session'):
            super().__del__()

    def __enter__(self):
        type(self).get_contexts().append(self)

        return self

    def __exit__(self, exc_type, exc_value, exc_trace):
        type(self).get_contexts().pop()

        if exc_type is not None:
            logger.error('%s: %s', exc_type.__name__, exc_value)

    @classmethod
    def get_contexts(cls):
        if not hasattr(cls.__context, 'stack'):
            cls.__context.stack = []

        return cls.__context.stack

    @classmethod
    def get_context(cls):
        """Return the deepest context on the stack."""
        try:
            return cls.get_contexts()[-1]
        except IndexError:
            raise TypeError("No context on context stack")

    def search(self, type, query, limit=1):
        """
        """
        results = super().search(query, type=type, limit=limit)

        return results[f'{type}s']['items']
