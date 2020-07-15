import logging
import threading
from abc import ABC
from queue import Queue

from ibranch.scraping_scheduler.configuration.Configurator import Configuration
from ibranch.scraping_scheduler.domain.System import Cache


class BaseJob(ABC):
    mutex = threading.Lock()

    def __init__(self, cache_name=None):
        self._logger = logging.getLogger(type(self).__name__)
        # Data queue
        # key = domain, value = url list
        if cache_name:
            self._cache_name = cache_name

            try:
                BaseJob.mutex.acquire(blocking=True)
                if Cache().cache_exists(self.cache_name):
                    cache_catalog = Cache().get_existing_cache(self.cache_name)
                else:
                    cache_catalog = Cache().get_new_cache(Queue)
            finally:
                BaseJob.mutex.release()
            Cache().register_catelog(self.cache_name, cache_catalog)
            self._cache = cache_catalog

    def run(self):
        raise NotImplementedError()

    @property
    def logger(self):
        return self._logger

    @property
    def cache_name(self):
        try:
            getattr(self, '_cache_name')
        except:
            raise NotImplementedError('Cache is permanently unavailable for this class')
        return self._cache_name

    @property
    def cache(self):
        return self._cache

    @property
    def schedule_type(self):
        return Configuration().getProperty(f"jobs.list.{type(self).__name__}.type")

    @property
    def cron(self):
        return Configuration().getProperty(f"jobs.list.{type(self).__name__}.cron")

    @property
    def sec(self):
        return Configuration().getProperty(f"jobs.list.{type(self).__name__}.sec")
