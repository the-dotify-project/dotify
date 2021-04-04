from functools import update_wrapper
from typing import Any, Optional


class classproperty:
    def __init__(self, method):
        self.method = method

        update_wrapper(self, method)

    def __get__(self, obj: Optional[Any], objtype: Optional[Any] = None) -> Any:
        return self.method(objtype)


class cached_classproperty(classproperty):
    def __init__(self, method):
        super().__init__(method)

        self.cache = None

    def __get__(self, obj: Optional[Any], objtype: Optional[Any] = None) -> Any:
        if self.cache is None:
            self.cache = super().__get__(obj, objtype=objtype)

        return self.cache
