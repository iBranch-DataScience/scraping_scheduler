from singleton_decorator import singleton


@singleton
class Cache:
    def __init__(self):
        self._cache_catalog = dict()

    def get_new_cache(self, data_structure_func=None):
        return data_structure_func()

    def register_catelog(self, cache_name: str, cache):
        self._cache_catalog[cache_name] = cache

    def remove_catelog(self, cache_name: str):
        del self._cache_catalog[cache_name]

    def cache_exists(self, cache_name):
        return cache_name in self._cache_catalog.keys()

    def get_existing_cache(self, cache_name: str):
        if cache_name not in self._cache_catalog.keys():
            raise LookupError(f"Cache catalog '{cache_name}' not exists! Current available: {self._cache_catalog.keys()}")
        return self._cache_catalog[cache_name]


class CONSTANT:
    @staticmethod
    def seed():
        return 77

    @staticmethod
    def presentation():
        return "presentation"

    @staticmethod
    def chrome_name():
        return "CHROME"

    @staticmethod
    def driver_name():
        return CONSTANT.chrome_name()
