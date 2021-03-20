import logging
from functools import wraps
from pathlib import Path
from re import match

from dotify.json_serializable import JsonSerializable
from spotipy.exceptions import SpotifyException


class Model(JsonSerializable):
    # FIXME: Consider defining a metaclass
    # for dynamically importing string type dependencies
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

    def __repr__(self):
        return f'<{self.__class__.__name__} "{str(self)}">'

    @classmethod
    def view_name(cls):
        return cls.__name__.lower()

    @classmethod
    def search(cls, query, limit=1):
        view_name = cls.view_name()

        results = cls.client.search(view_name, query, limit=limit)

        if not results:
            raise cls.NotFound

        return map(lambda kwargs: cls(**kwargs), results)

    @classmethod
    def validate_url(cls, method):
        @wraps(method)
        def wrapper(cls, url, *args, **kwargs):
            view_name = cls.view_name()
            pattern = f'https://open.spotify.com/{view_name}'

            try:
                assert match(pattern, url) is not None
            except AssertionError:
                cls.InvalidURL

            return method(cls, url, *args, **kwargs)

        return wrapper

    @classmethod
    def convert_to_model_error(cls, method):
        @wraps(method)
        def wrapper(cls, *args, **kwargs):
            try:
                return method(cls, *args, **kwargs)
            except SpotifyException as e:
                if e.http_status == 404:
                    raise cls.NotFound
                elif e.http_status == 400:
                    raise cls.InvalidURL
                else:
                    raise

        return wrapper
