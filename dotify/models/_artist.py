import logging
from typing import AnyStr, cast

from dotify._model import Model, logger

logger = logging.getLogger("{0}.{1}".format(logger.name, __name__))


class Artist(Model):
    """A class representing a Spotify `Artist`."""

    @property
    def url(self) -> AnyStr:
        """Return the artist's Spotify URL.

        Returns:
            AnyStr: the URL in string format
        """
        return cast(AnyStr, self.external_urls.spotify)

    def __str__(self) -> AnyStr:
        return cast(AnyStr, self.name)
