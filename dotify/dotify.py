import logging
import threading
from typing import Any, Dict, List

from spotipy import Spotify as Client
from spotipy.client import logger
from spotipy.oauth2 import SpotifyClientCredentials

logger = logging.getLogger(f"{logger.name}.{__name__}")


class Dotify(Client):
    """
    Example Usage:
        >>> from dotify import Dotify
        ... with Dotify(spotify_client, spotify_secret):
        ...     for result in Track.search(query):
        ...         ...
    """

    _context = threading.local()

    def __init__(self, client_id: str, client_secret: str) -> None:
        """Create a `Dotify` instance

        Args:
            client_id (str): your Spotify API client ID
            client_secret (str): your Spotify API client secret
        """
        super().__init__(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=client_id, client_secret=client_secret
            )
        )

    def __del__(self):
        if hasattr(self, "_session"):
            super().__del__()

    def __enter__(self) -> "Dotify":
        type(self).get_contexts().append(self)

        return self

    def __exit__(self, exc_type: None, exc_value: None, exc_trace: None) -> None:
        type(self).get_contexts().pop()

        if exc_type is not None:
            logger.error("%s: %s", exc_type.__name__, exc_value)

    @classmethod
    def get_contexts(cls) -> List["Dotify"]:
        """Get the `Dotify` context stack

        Returns:
            List[Dotify]: the `Dotify` context stack
        """
        if not hasattr(cls._context, "stack"):
            cls._context.stack = []

        return cls._context.stack

    @classmethod
    def get_context(cls) -> "Dotify":
        """Get the topmost context from the stack

        Raises:
            TypeError: if the context stack is empty

        Returns:
            Dotify: the topmost context
        """
        try:
            return cls.get_contexts()[-1]
        except IndexError:
            raise TypeError("No context on context stack")

    def search(self, type: str, query: str, limit: int = 1) -> List[Dict[str, Any]]:
        """Perform a Spotify search given a `query`

        Args:
            type (str): One of 'artist', 'album', 'track', 'playlist'
            query (str): the search `query`
            limit (int, optional): the number of items to return. Defaults to 1.

        Returns:
            List[Dict[str, Any]]: A list containing the search results
        """
        results = super().search(query, type=type, limit=limit)

        return results[f"{type}s"]["items"]
