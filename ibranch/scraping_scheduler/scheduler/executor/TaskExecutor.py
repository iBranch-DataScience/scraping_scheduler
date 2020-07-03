import logging
from abc import abstractmethod
from concurrent.futures.thread import ThreadPoolExecutor

from singleton_decorator import singleton

from ibranch.scraping_scheduler.configuration.Configurator import Configuration


class BaseExecutor:

    @abstractmethod
    def submit_tasks(self, tasks):
        pass

    @abstractmethod
    def shutdown(self):
        pass


@singleton
class ThreadExecutor(BaseExecutor):
    def __init__(self):
        self._logger = logging.getLogger(type(self).__name__)
        cfg = Configuration()
        job_lists = cfg.getProperty("jobs.list")

        self._pools = dict()
        for job_name, job_config in job_lists.items():
            pool_size = 1
            if 'one-off' != job_config["type"]:
                pool_size = job_config["pool_size"]
            max_workers = pool_size

            # Configure worker
            thread_pool_executor = ThreadPoolExecutor(
                thread_name_prefix=f'task_executor_{job_name}',
                max_workers=max_workers)
            self._pools[job_name] = thread_pool_executor

    def submit_tasks(self, job_type, tasks):
        thread_pool_executor = self._pools[job_type]
        [thread_pool_executor.submit(task.run) for task in tasks]

    def shutdown(self):
        [thread_pool_executor.shutdown() for thread_pool_executor in self._pools.values()]
