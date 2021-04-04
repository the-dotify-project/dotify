import logging
from functools import wraps
from importlib import import_module
from pathlib import Path
from re import match
from typing import Iterator

from spotipy.exceptions import SpotifyException

from dotify.decorators import cached_classproperty, classproperty
from dotify.dotify import Dotify
from dotify.json_serializable import (JsonSerializable, JsonSerializableMeta,
                                      logger)

logger = logging.getLogger(f'{logger.name}.{__name__}')


class ModelMeta(JsonSerializableMeta):
    """ """
    schema_dir = Path(__file__).parent / 'models' / 'schema'

    @staticmethod
    def dependency_basename(class_name: str) -> str:
        return f'{class_name.lower()}.json'

    def __new__(cls, name, bases, attrs):
        if 'Json' in attrs:
            attrs['Json'].schema = cls.schema_dir / cls.dependency_basename(name)

            if hasattr(attrs['Json'], 'dependencies'):
                dependency_names = attrs['Json'].dependencies

                @cached_classproperty
                def dependencies(_):
                    types = []
                    for dependency in dependency_names:
                        module, _, type = dependency.rpartition('.')

                        module = import_module(module)
                        type = getattr(module, type)

                        types.append(type)

                    return {
                        cls.dependency_basename(dependency.__name__): dependency
                        for dependency in types
                    }

                attrs['Json'].dependencies = dependencies

        return super().__new__(cls, name, bases, attrs)


class Model(JsonSerializable, metaclass=ModelMeta):
    """ """
    class InvalidURL(Exception):
        """ """
        pass

    class NotFound(Exception):
        """ """
        pass

    def __repr__(self):
        return f'<{self.__class__.__name__} "{str(self)}">'

    @classproperty
    def context(cls):
        return Dotify.get_context()

    @classmethod
    def view_name(cls) -> str:
        """ """
        return cls.__name__.lower()

    @classmethod
    def search(cls, query: str, limit: int = 1) -> Iterator["Model"]:
        """
        """
        view_name = cls.view_name()

        results = cls.context.search(view_name, query, limit=limit)

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
