from pathlib import Path

import dotify.models.model as base


class Artist(base.Model):
    """ """
    class Json:
        """ """
        schema = base.Model.Json.schema_dir / 'artist.json'

    @property
    def url(self):
        """ """
        return self.external_urls.spotify

    def __str__(self):
        return self.name
