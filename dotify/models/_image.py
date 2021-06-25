import logging

from dotify._model import Model, logger

logger = logging.getLogger("{0}.{1}".format(logger.name, __name__))


class Image(Model):
    """A class representing a Spotify `Image`."""

    def __str__(self):
        return self.url
