from pathlib import Path

import dotify.models.base as base


class User(base.Base):
    class Json:
        schema = base.Base.Json.schema_dir / 'user.json'
