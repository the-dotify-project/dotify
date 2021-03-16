import logging
from pathlib import Path
from re import match

from dotify.json_serializable import JsonSerializable, JsonSerializableMeta


class Base(JsonSerializable):
    class Json:
        schema_dir = Path(__file__).parent / 'schema'

    logger: logging.Logger

    class InvalidURL(Exception):
        pass

    class NotFound(Exception):
        pass

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        name = self.__class__.__name__
        if hasattr(self, 'client'):
            name = f'{self.client.logger.name}.{name}'

        self.logger = logging.getLogger(name)

    @classmethod
    def view_name(cls):
        return cls.__name__.lower()

    @classmethod
    def assert_valid_url(cls, url):
        view_name = cls.view_name()
        pattern = f'https://open.spotify.com/{view_name}'

        try:
            assert match(pattern, url) is not None
        except AssertionError:
            cls.InvalidURL(f'{url} is not a valid spotify {view_name} url')

    @classmethod
    def search(cls, query, limit=1):
        view_name = cls.view_name()

        results = cls.client.search(view_name, query, limit=limit)

        if not results:
            raise cls.NotFound

        return map(lambda kwargs: cls(**kwargs), results)

    @classmethod
    def get(cls, url):
        view_name = cls.view_name()

        try:
            return cls.client.get(view_name, url)
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 404:
                raise cls.NotFound
            elif e.http_status == 400:
                raise cls.InvalidURL
            else:
                raise
