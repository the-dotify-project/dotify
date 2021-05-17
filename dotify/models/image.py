import logging

from dotify.model import Model, logger

logger = logging.getLogger(f"{logger.name}.{__name__}")


class Image(Model):
    """ """

    class Json(object):
        """ """

    def __str__(self):
        return self.url
