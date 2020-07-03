import threading

from singleton_decorator import singleton

from ibranch.scraping_scheduler.configuration.Configurator import Configuration


@singleton
class FlowShaper:
    def __init__(self):
        cfg = Configuration()
        cache_types = cfg.getProperty("traffic_limit").keys()

        self._mutexes = dict()
        for cache_type in cache_types:
            limit = cfg.getProperty(f"traffic_limit.{cache_type}.size")

            # Configure limit
            self._mutexes[cache_type] = threading.Semaphore(limit)

    def get(self, type_name, limit=None):
        return self._mutexes[type_name]

    def release(self, type_name):
        self._mutexes[type_name].release()

    def acquire(self, type_name):
        return self._mutexes[type_name].acquire(blocking=False)
