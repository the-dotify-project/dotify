import contextlib
import logging
import os
import threading
from typing import Any, AnyStr, Dict, List, Optional, cast

from spotipy import Spotify as Client
from spotipy.client import logger
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOauthError

from dotify._decorators import classproperty

logger = logging.getLogger("{0}.{1}".format(logger.name, __name__))


class Dotify(Client):
    """A subclass of `spotipy.Spotify`, which provides a more object oriented interface.

    Examples:
        >>> from dotify import Dotify
        ... with Dotify(spotify_client, spotify_secret):
        ...     for result in Track.search(query):
        ...         ...
    """

    _context = threading.local()

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
    ) -> None:
        """Create a `Dotify` instance.

        If no `client_id` and/or `client_secret` are provided, an environment
        variable look up is performed for the names `SPOTIFY_ID` and/or `SPOTIFY_SECRET`.

        Args:
            client_id (Optional[str]): your Spotify API client ID. Defaults to None
            client_secret (Optional[str]): your Spotify API client secret. Defaults to None

        Raises:
            TypeError: In case the supplied credentials are invalid
        """
        if client_id is None:
            client_id = os.getenv("SPOTIFY_ID")

        if client_secret is None:
            client_secret = os.getenv("SPOTIFY_SECRET")

        try:
            super().__init__(
                client_credentials_manager=SpotifyClientCredentials(
                    client_id=client_id,
                    client_secret=client_secret,
                ),
            )
        except SpotifyOauthError as oauth_error:
            raise TypeError("Invalid Credentials") from oauth_error

    def __del__(self):
        with contextlib.suppress(AttributeError):
            super().__del__()

    def __enter__(self) -> "Dotify":
        type(self).contexts.append(self)

        return self

    def __exit__(self, exc_type, exc_value, _) -> None:
        type(self).contexts.pop()

        if exc_type is not None:
            logger.error("%s: %s", exc_type.__name__, exc_value)

    @classproperty
    def contexts(cls) -> List["Dotify"]:
        """Get the `Dotify` context stack.

        Returns:
            List[Dotify]: the `Dotify` context stack
        """
        try:
            return cast(Dotify, cls._context.stack)
        except AttributeError:
            cls._context.stack = []

            return cls._context.stack

    @classproperty
    def context(cls) -> Optional["Dotify"]:
        """Get the topmost context from the stack.

        Returns:
            Optional[Dotify]: the topmost context
        """
        try:
            return cast(Dotify, cls.contexts[-1])
        except IndexError:
            return None

    def search(
        self,
        model_type: str,
        query: AnyStr,
        limit: Optional[int] = 1,
    ) -> List[Dict[AnyStr, Any]]:
        """Perform a Spotify search given a `query`.

        Args:
            model_type (str): One of 'artist', 'album', 'track', 'playlist'
            query (AnyStr): the search `query`
            limit (Optional[int]): the number of items to return. Defaults to 1.

        Returns:
            List[Dict[AnyStr, Any]]: A list containing the search results
        """
        results = super().search(query, type=model_type, limit=limit)

        return cast(
            List[Dict[AnyStr, Any]],
            results[
                "{0}s".format(
                    model_type,
                )
            ]["items"],
        )
