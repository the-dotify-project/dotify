
import logging
from re import match

from dotify.json_serializable import JsonSerializable, JsonSerializableMeta


class DotifyMeta(JsonSerializableMeta):
    class InvalidURL(Exception):
        pass

    class NotFound(Exception):
        pass

    def __new__(cls, name, bases, attrs):
        attrs['InvalidURL'] = DotifyMeta.InvalidURL
        attrs['NotFound'] = DotifyMeta.NotFound

        return super().__new__(cls, name, bases, attrs)


class Base(JsonSerializable, metaclass=DotifyMeta):
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
