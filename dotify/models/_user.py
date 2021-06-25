import logging

from dotify._model import Model, logger

logger = logging.getLogger("{0}.{1}".format(logger.name, __name__))


class User(Model):
    """A model representing a Spotify `User`."""

    def __str__(self):
        return self.display_name
