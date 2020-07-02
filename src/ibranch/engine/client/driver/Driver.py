import os

from scraping_scheduler.ibranch.configuration.Configurator import Configuration
from scraping_scheduler.ibranch.domain.System import CONSTANT
from selenium import webdriver
from singleton_decorator import singleton


@singleton
class DriverBuilder:
    def __init__(self):
        self._use_headless = False
        self._browser_type = CONSTANT.driver_name()
        cfg = Configuration()
        self._driver_path_mapping = {
            CONSTANT.chrome_name(): cfg.getProperty("driver_path.chrome")
        }
        self._driver_builder_mapping = {
            CONSTANT.chrome_name(): self._build_chrome_driver
        }
        self._clear_process_cmd_mapping = {
            CONSTANT.chrome_name(): self._clear_chrome_process
        }
        self._tmp_dir = cfg.getProperty("client.tmp_dir")
        options = webdriver.ChromeOptions()
        if self._use_headless:
            options.add_argument('headless')
        cfg = {'download.default_directory': self._tmp_dir}
        options.add_experimental_option('prefs', cfg)
        options.add_argument(f"download.default_directory={self._tmp_dir}")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--hide-scrollbars')
        self._options = options

        self._driver_path = self._driver_path_mapping.get(self._browser_type)
        self._safe_raise_exception(self._driver_path, f"Driver for browser {self._browser_type} not configured! ")
        os.environ['PATH'] += os.pathsep + self._driver_path
        self._builder = self._driver_builder_mapping.get(self._browser_type)
        self._safe_raise_exception(self._builder, f"Browser {self._browser_type} not supported")

    @property
    def browser_type(self):
        return self._browser_type

    @property
    def driver_path(self):
        return self._driver_path

    @property
    def use_headless(self):
        return self._use_headless

    def _safe_raise_exception(self, obj_to_check, err_msg):
        if obj_to_check is None:
            raise Exception(err_msg)

    def build(self):
        return self._builder()

    def _build_chrome_driver(self):
        driver = webdriver.Chrome(options=self._options)
        driver.maximize_window()
        return driver

    def _clear_chrome_process(self):
        os.system("pkill chrome")

    def clear_browser_process(self):
        cleaning_cmd = self._clear_process_cmd_mapping.get(self._browser_type)
        cleaning_cmd()
