from abc import ABC

from scraping_scheduler.ibranch.configuration.Configurator import Configuration


class BaseJob(ABC):
    def __init__(self, cache_name=None):
        # Data queue
        # key = domain, value = url list
        if cache_name:
            self._cache_name = cache_name

    def run(self):
        raise NotImplementedError()

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
    def job_class(self):
        raise NotImplementedError()

    @property
    def schedule_type(self):
        return Configuration().getProperty(f"schedule.{self.job_class}.type")

    @property
    def cron(self):
        return Configuration().getProperty(f"schedule.{self.job_class}.cron")

    @property
    def sec(self):
        return Configuration().getProperty(f"schedule.{self.job_class}.sec")
