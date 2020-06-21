import logging
from abc import abstractmethod
from concurrent.futures.thread import ThreadPoolExecutor

from singleton_decorator import singleton

from scraping_scheduler.ibranch.configuration.Configurator import Configuration


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
        pool_types = cfg.getProperty("thread_pool").keys()

        self._pools = dict()
        for pool_type in pool_types:
            max_workers = cfg.getProperty(f"thread_pool.{pool_type}.size")

            # Configure worker
            thread_pool_executor = ThreadPoolExecutor(
                thread_name_prefix=f'task_executor_{pool_type}',
                max_workers=max_workers)
            self._pools[pool_type] = thread_pool_executor

    def submit_tasks(self, pool_type, tasks):
        thread_pool_executor = self._pools[pool_type]
        [thread_pool_executor.submit(task.run) for task in tasks]

    def shutdown(self):
        [thread_pool_executor.shutdown() for thread_pool_executor in self._pools.values()]
