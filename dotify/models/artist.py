import logging

from dotify.model import Model, logger

logger = logging.getLogger(f'{logger.name}.{__name__}')


class Artist(Model):
    """ """
    class Json:
        """ """
        schema = 'artist.json'

    @property
    def url(self):
        """ """
        return self.external_urls.spotify

    def __str__(self):
        return self.name
