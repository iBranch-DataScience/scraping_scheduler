import logging
from importlib import import_module

from ibranch.scraping_scheduler.configuration.Configurator import Configuration
from ibranch.scraping_scheduler.scheduler.ScrapeScheduler import ScrapeScheduler


class ScraperEngine:
    def __init__(self):
        self._logger = logging.getLogger(type(self).__name__)

        jobs = Configuration().getProperty('jobs')
        self._package = jobs.get("package")
        self._module = jobs.get("module")
        self._job_list = jobs.get("list")

        self._config_file_path = None

    def start(self):
        Job_Package = import_module('.%s' % self._module, package=self._package)

        with ScrapeScheduler() as scheduler:
            # Jobs:
            for job_config in self._job_list:
                job_name = list(job_config.keys())[0]
                job = getattr(Job_Package, job_name)
                scheduler.register_job(job())
            # Go
            scheduler.start()
