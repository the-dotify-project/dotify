import logging

from dotify.model import Model, logger

logger = logging.getLogger("{0}.{1}".format(logger.name, __name__))


class Artist(Model):
    """ """

    class Json(object):
        """ """

    @property
    def url(self):
        """ """
        return self.external_urls.spotify

    def __str__(self) -> str:
        return self.name
