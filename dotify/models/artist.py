from pathlib import Path

import dotify.models.base as base


class Artist(base.Base):
    class Json:
        schema = base.Base.Json.schema_dir / 'artist.json'

    @property
    def url(self):
        return self.external_urls.spotify
