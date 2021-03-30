from functools import update_wrapper


class cached_classproperty:
    def __init__(self, method):
        self.method = method
        self.cache = None

        update_wrapper(self, method)

    def __get__(self, obj, objtype=None):
        if self.cache is None:
            self.cache = self.method(objtype)

        return self.cache
