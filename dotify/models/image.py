from pathlib import Path

import dotify.models.model as base


class Image(base.Model):
    class Json:
        schema = base.Model.Json.schema_dir / 'image.json'
