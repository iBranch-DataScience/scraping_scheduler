import json

import requests
from singleton_decorator import singleton

from scraping_scheduler.ibranch.configuration.Configurator import Configuration
from scraping_scheduler.ibranch.util.Toolbox import Formatter


def _inject_session(func):
    def _wrapper(*args, **kwargs):
        with requests.sessions.Session() as session:
            session.keep_alive = False
            args = list(args)
            args[1] = session
            x = func(*args, **kwargs)
            return x

    return _wrapper


def _check_reponse_type(func):
    def _wrapper(*args, **kwargs):
        if not isinstance(args[0], requests.Response):
            raise TypeError(f'Expected: {requests.Response}, actual: {type(args[0])} ')
        return func(*args, **kwargs)

    return _wrapper


@singleton
class ClientFactory:
    def __init__(self):
        cfg = Configuration()
        self._timeout = cfg.getProperty("client.requests.timeout")

    def build(self):
        return Client(self._timeout)


class Client:
    def __init__(self, timeout):
        self._timeout = timeout
        self._response = None

    @_inject_session
    def _get(self, session, url):
        self._response = session.get(url=url, timeout=self._timeout)
        return self

    def get(self, url):
        return self._get(None, url)

    def get_header(self):
        return self._response.headers

    def is_success(self):
        return self.get_html_status_code() == 200

    def get_html_status_code(self):
        return self._response.status_code

    def get_source_code(self):
        return self._response.text

    def get_header_map(self):
        return Formatter.to_lower_case_dict(self._response.headers)

    def is_text_transmission(self):
        if 'content-type' not in self.get_header_map():
            return False
        return 'text/' in self.get_header_map()['content-type']

    def get_json(self):
        return self._response.json()

    def get_header_dump(self):
        return json.dumps(self.get_header_map())
