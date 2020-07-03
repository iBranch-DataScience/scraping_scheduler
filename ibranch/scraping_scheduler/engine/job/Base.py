from abc import ABC

from ibranch.scraping_scheduler.configuration.Configurator import Configuration


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
        return self._get_config()[self.__class__.__name__]['type']

    @property
    def cron(self):
        return self._get_config()[self.__class__.__name__]['cron']

    @property
    def sec(self):
        return self._get_config()[self.__class__.__name__]['sec']

    def _get_config(self):
        job_list = Configuration().getProperty("jobs.list")
        job = [job_config for job_config in job_list if self.__class__.__name__ in job_config]
        if len(job) == 0:
            raise AttributeError(f'{self.__class__.__name__} not configured')
        if len(job) > 1:
            raise AttributeError(f'{self.__class__.__name__} configured multiple times')
        return job[0]
