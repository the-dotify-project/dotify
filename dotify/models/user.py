import logging

from dotify.model import Model, logger

logger = logging.getLogger(f'{logger.name}.{__name__}')


class User(Model):
    """ """
    class Json:
        """ """

    def __str__(self):
        return self.display_name
