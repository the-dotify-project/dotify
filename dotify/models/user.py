import logging

from dotify.model import Model, logger

logger = logging.getLogger(f'{logger.name}.{__name__}')


class User(Model):
    """ """
    class Json:
        """ """
        schema = 'user.json'
