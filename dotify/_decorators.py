from functools import update_wrapper
from typing import Any, Callable, Optional


class classproperty(object):
    """
    A decorator that converts a method to a `classproperty`.

    Examples:
        >>> from random import random
        >>> class Foo:
        ...     @classproperty
        ...     def bar(cls):
        ...         return
        ...
        >>> Foo.bar
        0.6597781045639168
        >>> Foo.bar
        0.45628230476739395
    """

    def __init__(self, method: Callable[..., Any]) -> None:
        """Create a `classproperty` instance.

        Args:
            method (Callable[..., Any]): the method being decorated
        """
        self.method = method

        update_wrapper(self, method)

    def __get__(self, obj: Optional[Any], objtype: Optional[Any] = None) -> Any:
        return self.method(objtype)


class cached_classproperty(classproperty):
    """A decorator that converts a method to a `cached_classproperty`.

    As indicated by the name, once the method is called, its
    return value is cached and is therefore returned unchanged.

    Examples:
        >>> from random import random
        >>> class Foo:
        ...     @cached_classproperty
        ...     def bar(cls):
        ...         return
        ...
        >>> Foo.bar
        0.6597781045639168
        >>> Foo.bar
        0.6597781045639168
    """

    def __init__(self, method: Callable[..., Any]) -> None:
        """Create a `cached_classproperty` instance.

        Args:
            method (Callable[..., Any]): the method being decorated
        """
        super().__init__(method)

        self.cache = None

    def __get__(self, obj: Optional[Any], objtype: Optional[Any] = None) -> Any:
        if self.cache is None:
            self.cache = super().__get__(obj, objtype=objtype)

        return self.cache
