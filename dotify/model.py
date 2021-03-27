import logging
from functools import wraps
from pathlib import Path
from re import match

from spotipy.exceptions import SpotifyException

from dotify.dotify import Dotify
from dotify.json_serializable import (JsonSerializable, JsonSerializableMeta,
                                      logger)

logger = logging.getLogger(f'{logger.name}.{__name__}')


class ModelMeta(JsonSerializableMeta):
    """ """
    BASE_DIR = Path(__file__).parent / 'models' / 'schema'

    def __new__(cls, name, bases, attrs):
        if 'Json' not in attrs:
            return super().__new__(cls, name, bases, attrs)

        if hasattr(attrs['Json'], 'schema'):
            attrs['Json'].schema = ModelMeta.BASE_DIR / attrs['Json'].schema

            return super().__new__(cls, name, bases, attrs)

        return super().__new__(cls, name, bases, attrs)


class Model(JsonSerializable, metaclass=ModelMeta):
    """ """
    # FIXME: Consider defining a metaclass
    # for dynamically importing string type dependencies

    class InvalidURL(Exception):
        """ """
        pass

    class NotFound(Exception):
        """ """
        pass

    def __repr__(self):
        return f'<{self.__class__.__name__} "{str(self)}">'

    @classmethod
    def view_name(cls):
        """ """
        return cls.__name__.lower()

    @classmethod
    def search(cls, query, limit=1):
        """
        """
        view_name = cls.view_name()

        results = Dotify.get_context().search(view_name, query, limit=limit)

        if not results:
            raise cls.NotFound

        return map(lambda kwargs: cls(**kwargs), results)

    @classmethod
    def validate_url(cls, method):
        """
        """
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
        """
        """
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
