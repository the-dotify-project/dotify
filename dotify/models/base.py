
import logging
from re import match

from dotify.json_serializable import JsonSerializable, JsonSerializableMeta
from dotify.resolver import RelativePathRefResolver


class Base(JsonSerializable):
    logger: logging.Logger

    class InvalidURL(Exception):
        pass

    class NotFound(Exception):
        pass

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        name = self.view_name()
        if hasattr(self, 'client'):
            name = f'{self.client.logger.name}.{name}'

        self.logger = logging.getLogger(name)

    @classmethod
    def view_name(cls):
        return cls.__name__

    @classmethod
    def assert_valid_url(cls, url):
        view_name = cls.view_name().lower()
        pattern = f'https://open.spotify.com/{view_name}'

        try:
            assert match(pattern, url) is not None
        except AssertionError:
            cls.InvalidURL(f'{url} is not a valid spotify {view_name} url')

    @classmethod
    def search(cls, query, limit=1):
        view_name = cls.view_name().lower()

        return map(
            lambda kwargs: cls(**kwargs),
            cls.client.search(query, view_name, limit=limit)
        )
