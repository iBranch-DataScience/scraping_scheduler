import threading

from singleton_decorator import singleton

from org.ibranch.configuration.Configurator import Configuration


@singleton
class FlowShaper:
    def __init__(self):
        cfg = Configuration()
        pool_types = cfg.getProperty("thread_pool").keys()

        self._mutexes = dict()
        for pool_type in pool_types:
            limit = cfg.getProperty(f"thread_pool.{pool_type}.size")

            # Configure limit
            self._mutexes[pool_type] = threading.Semaphore(limit)

    def get(self, type_name, limit=None):
        return self._mutexes[type_name]

    def release(self, type_name):
        self._mutexes[type_name].release()

    def acquire(self, type_name):
        return self._mutexes[type_name].acquire(blocking=False)
