import logging

from dotify.model import Model, logger

logger = logging.getLogger(f"{logger.name}.{__name__}")


class User(Model):
    """A model representing a Spotify User"""

    class Json:
        pass

    def __str__(self):
        return self.display_name
