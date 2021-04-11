import logging
from functools import wraps
from importlib import import_module
from os import PathLike
from pathlib import Path
from re import match
from typing import Any, Callable, Iterator

from spotipy.exceptions import SpotifyException

from dotify.decorators import cached_classproperty
from dotify.dotify import Dotify
from dotify.json_serializable import JsonSerializable, JsonSerializableMeta, logger

logger = logging.getLogger(f"{logger.name}.{__name__}")


class ModelMeta(JsonSerializableMeta):
    """
    A metaclass serving as an abstraction layer over
    the `JsonSerializableMeta` metaclass, that automatically
    resolves the path to the `Model`'s JSON schema, as well as
    builds the `dependency` dictionary
    """

    @classmethod
    def dependency_basename(cls, model_name: str) -> str:
        """Given the name of a `Model` resolve the basename of
        the corresponding json schema

        Args:
            model_name (str): the name of a `Model`

        Returns:
            str: the basename of the file containing the json schema
        """
        return f"{model_name.lower()}.json"

    @classmethod
    def dependency_path(cls, model_name: str) -> PathLike:
        """Given the name of a `Model` resolve the path to
        the corresponding json schema

        Args:
            model_name (str): the name of a `Model`

        Returns:
            PathLike: the path to the file containing the json schema
        """
        return (
            Path(__file__).parent
            / "models"
            / "schema"
            / cls.dependency_basename(model_name)
        )

    def __new__(cls, name, bases, attrs):
        if "Json" in attrs:
            attrs["Json"].schema = cls.dependency_path(name)

            if hasattr(attrs["Json"], "dependencies"):
                dependency_names = attrs["Json"].dependencies

                @cached_classproperty
                def dependencies(_):
                    types = []
                    for dependency in dependency_names:
                        module, _, type = dependency.rpartition(".")

                        module = import_module(module)
                        type = getattr(module, type)

                        types.append(type)

                    return {
                        cls.dependency_basename(dependency.__name__): dependency
                        for dependency in types
                    }

                attrs["Json"].dependencies = dependencies

        return super().__new__(cls, name, bases, attrs)


class Model(JsonSerializable, metaclass=ModelMeta):
    """
    The base class for every Spotify Web API entity
    """

    class UnexpectedError(Exception):
        """An exception indicating an unexpected error"""

        pass

    class InvalidURL(Exception):
        """
        An exception thrown if the provided URL does not
        correspond to a valid Spotify URL
        """

        pass

    class NotFound(Exception):
        """
        An exception thrown if an operation fails to
        retrieve the necessary information
        """

        pass

    def __repr__(self):
        return f'<{self.__class__.__name__} "{str(self)}">'

    @cached_classproperty
    def context(cls) -> Dotify:
        """Get the current `Dotify` context

        Returns:
            Dotify: the current `Dotify` context
        """
        return Dotify.get_context()

    @classmethod
    def view_name(cls) -> str:
        """Return the name of the Spotify view corresponding to the `Model`

        Returns:
            str: the name of the Spotify view
        """
        return cls.__name__.lower()

    @classmethod
    def search(cls, query: str, limit: int = 1) -> Iterator["Model"]:
        """Perform a Spotify search given a `query`

        Args:
            query (str): the search `query`
            limit (int, optional): the number of items to return. Defaults to 1.

        Raises:
            cls.NotFound: In case no results corresponding to the provided query
            are found

        Returns:
            Iterator["Model"]: the `Model` instances corresponding to the query
        """
        view_name = cls.view_name()

        results = cls.context.search(view_name, query, limit=limit)

        if not results:
            raise cls.NotFound

        return map(lambda kwargs: cls(**kwargs), results)

    @classmethod
    def validate_url(cls, method: Callable[..., Any]) -> Callable[..., Any]:
        """A decorator that validates the supplied `URL`
        before executing the decorated method

        Args:
            method (Callable[..., Any]): the method being decorated

        Raises:
            cls.InvalidURL: in case the supplied url is invalid

        Returns:
            Callable[..., Any]: the  decorated method
        """

        @wraps(method)
        def wrapper(cls, url, *args, **kwargs):
            view_name = cls.view_name()
            pattern = f"https://open.spotify.com/{view_name}"

            try:
                assert match(pattern, url) is not None
            except AssertionError:
                raise cls.InvalidURL from None

            return method(cls, url, *args, **kwargs)

        return wrapper

    @classmethod
    def http_safeguard(cls, method: Callable[..., Any]) -> Callable[..., Any]:
        """A decorator that converts http exceptions to `Model` level
        exceptions

        Args:
            method (Callable[..., Any]): the method being decorated

        Raises:
            cls.NotFound: in case a `Spotipy` call returns an HTTP status of 404
            cls.InvalidURL: in case a `Spotipy` call returns an HTTP status of 400
            cls.UnexpectedError: in case a `Spotipy` call returns any other HTTP status
            indicating an error

        Returns:
            Callable[..., Any]: the decorated method
        """

        @wraps(method)
        def wrapper(cls, *args, **kwargs):
            try:
                return method(cls, *args, **kwargs)
            except SpotifyException as e:
                if e.http_status == 404:
                    raise cls.NotFound from None
                elif e.http_status == 400:
                    raise cls.InvalidURL from None
                else:
                    raise cls.UnexpectedError from None

        return wrapper
