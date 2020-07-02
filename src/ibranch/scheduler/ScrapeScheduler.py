import logging
from abc import ABC, abstractmethod

from apscheduler.events import EVENT_JOB_ERROR
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from scraping_scheduler.ibranch.engine.job.Base import BaseJob
from scraping_scheduler.ibranch.scheduler.executor.TaskExecutor import ThreadExecutor as TaskExecutor
from scraping_scheduler.ibranch.util.Toolbox import Formatter
from scraping_scheduler.ibranch.util.Toolbox import LogicUtil


class Executor(ABC):
    @abstractmethod
    def start(self):
        pass


class ScrapeScheduler(Executor):

    def __init__(self):
        Executor.register(ScrapeScheduler)
        self._logger = logging.getLogger(type(self).__name__)
        self._scheduler = None
        self._executor = None
        self._job_list = list()


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._executor.shutdown()

    def register_cache(self, cache_name):
        self._cache.register_catelog(cache_name)

    def register_job(self, job: BaseJob):
        '''
        Default to run every minute
        :param job:
        :return:
        '''
        self._job_list.append(job)

    def _create_executors(self):
        max_instances = len([job for job in self._job_list if job.schedule_type != 'one-off'])
        max_instances = LogicUtil.if_else_default(max_instances, 1, lambda x: x > 0)
        job_defaults = {'max_instances': max_instances}
        self._scheduler = BlockingScheduler(job_defaults=job_defaults)
        self._executor = TaskExecutor()

    def _add_hooks(self):
        _self = self

        def shutdown_hook(event):
            e = event.exception
            if e:
                _self._logger.error(f'{Formatter.get_timestamp()} - Scheduler crashed!, {type(e)} - {e}')
                if isinstance(e, KeyboardInterrupt):
                    if None is not _self._scheduler:
                        _self._scheduler.remove_all_jobs()
                        _self._scheduler.shutdown()
                    if None is not _self._executor:
                        _self._executor.shutdown()

        self._scheduler.add_listener(shutdown_hook, EVENT_JOB_ERROR)

    def _add_registred_jobs(self):
        for job in self._job_list:
            if job.schedule_type == "sec":
                self._scheduler.add_job(job.run,
                                        'interval',
                                        id=type(job).__name__,
                                        seconds=job.sec)
            elif job.schedule_type == "cron":
                self._scheduler.add_job(job.run,
                                        CronTrigger.from_crontab(job.cron),
                                        id=type(job).__name__)
            elif job.schedule_type == "one-off":
                self._scheduler.add_job(job.run,
                                        id=type(job).__name__)

    def start(self):
        # Lazy init
        self._create_executors()
        self._add_hooks()
        self._add_registred_jobs()

        self._scheduler.start()

    def shutdown(self):
        self._scheduler.shutdown()
