import logging
import os
from threading import Timer

from selenium.common.exceptions import NoAlertPresentException, \
    UnexpectedAlertPresentException, JavascriptException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from singleton_decorator import singleton

from ibranch.scraping_scheduler.configuration.Configurator import Configuration
from ibranch.scraping_scheduler.engine.client.driver.Driver import DriverBuilder


@singleton
class SeleniumClientBuilder:
    def __init__(self):
        os.environ["DBUS_SESSION_BUS_ADDRESS"] = "/dev/null"
        cfg = Configuration()
        self._timeout = cfg.getProperty("client.selenium.timeout")

    def build(self):
        return Client(self._timeout)


class Client:
    '''
        Not thread safe
    '''

    def __init__(self, timeout):
        self._logger = logging.getLogger(type(self).__name__)
        self._timeout = timeout
        self._driver = DriverBuilder().build()
        self._driver.implicitly_wait(self._timeout)

    '''
        timeout_coef is used to give the program extra time to execute
    '''
    def scrape(self, target_url, timeout_lambda, timeout_coef):
        driver = self._driver
        timeout = self._timeout * timeout_coef

        def force_close():
            driver.quit()
            timeout_lambda()
            self._logger.error(f'Long transaction detected, force to cut: {target_url}')
        t = Timer(timeout, force_close)
        t.start()
        self._logger.debug(f"Request url: {target_url}")
        self._driver.get(target_url)
        t.cancel()

    def open_url(self, url):
        self._driver.get(url)

    def input_text(self, text, element_name):
        self._driver.find_element_by_name(element_name).send_keys(text)

    def click(self, key_word):
        es = self._driver.find_elements_by_xpath("//a[@href]")
        e = None
        for element in es:
            href = element.get_attribute("href")
            if key_word in href:
                e = element
                break

        e.click()

    def enter(self):
        self._driver.switch_to.active_element.send_keys(Keys.ENTER)

    def click_alert(self):
        try:
            self._driver.switch_to.alert.accept()
        except NoAlertPresentException:
            pass

    def execute_script(self, script):
        self._driver.execute_script(script)

    def dismiss_dialog(self):
        try:
            self._driver.switch_to.alert.dismiss()
        except NoAlertPresentException:
            pass

    def remove_dom_element(self, element_id):
        try:
            self._driver.execute_script(f"document.getElementById('{element_id}').remove()")
        except JavascriptException as e:
            self._logger.error(f"Element Id{element_id} not found! ")
            raise e

    def wait_ready_by_dom_tag_name(self, tag_name="body"):
        self._wait_ready(By.TAG_NAME, tag_name)

    def wait_ready_by_dom_id(self, element_id):
        self._wait_ready(By.ID, element_id)

    def _wait_ready(self, by, value):
        try:
            # Wait
            WebDriverWait(self._driver, self._timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except UnexpectedAlertPresentException:
            self.click_alert()
        except StaleElementReferenceException:
            pass

    def get_source_code(self):
        return self._driver.page_source

    '''
        Return saved snapshot full path location
    '''
    def save_snapshot(self, file_path, file_name):
        png_file = os.path.join(file_path, file_name)
        try:
            self._driver.save_screenshot(png_file)
        except Exception as e:
            self._logger.error(f"Error on save screenshot: {e}")
            raise e

        return png_file

    def close(self):
        # Comment the logic for now, the IO might overwhelming if we call it frequently
        '''
        try:
            self.clear_cache()
        except Exception as e:
            self._logger.error(f"Error on cache cleaning: {e}")
        '''
        try:
            if self._driver is not None:
                pass
                self._driver.close()
                self._driver.quit()
        except AttributeError as ae:
            self._logger.error(f"Attribute error on close: {ae}")
            pass

    def get_clear_browsing_button(self):
        """Find the "CLEAR BROWSING BUTTON" on the Chrome settings page."""
        return self._driver.find_element_by_css_selector('* /deep/ #clearBrowsingDataConfirm')

    def clear_cache(self, timeout=60):
        """Clear the cookies and cache for the ChromeDriver instance."""
        # navigate to the settings page
        self._driver.get('chrome://settings/clearBrowserData')

        # wait for the button to appear
        wait = WebDriverWait(self._driver, timeout)
        wait.until(self.get_clear_browsing_button())

        # click the button to clear the cache
        self.get_clear_browsing_button().click()

        # wait for the button to be gone before returning
        wait.until_not(self.get_clear_browsing_button())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
