from pathlib import Path

import dotify.models.model as base


class User(base.Model):
    """ """
    class Json:
        """ """
        schema = base.Model.Json.schema_dir / 'user.json'
