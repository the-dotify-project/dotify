from pathlib import Path

import dotify.models.base as base


class Image(base.Base):
    class Json:
        schema = base.Base.Json.schema_dir / 'image.json'
