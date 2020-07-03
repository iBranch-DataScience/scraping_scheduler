import json

import requests
from singleton_decorator import singleton

from ibranch.scraping_scheduler.configuration.Configurator import Configuration
from ibranch.scraping_scheduler.util.Toolbox import Formatter


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


class Rensponse:
    def __init__(self, response):
        self._response = response

    @property
    def response(self):
        return self._response

    @property
    def header(self):
        return self._response.headers

    def is_success(self):
        return self.html_status_code == 200

    @property
    def html_status_code(self):
        return self._response.status_code

    @property
    def source_code(self):
        return self._response.text

    @property
    def header_map(self):
        return Formatter.to_lower_case_dict(self._response.headers)

    def is_text_transmission(self):
        if 'content-type' not in self.header_map:
            return False
        return 'text/' in self.header_map['content-type']

    @property
    def json(self):
        return self._response.json()

    @property
    def header_dump(self):
        return json.dumps(self.header_map)


class Client:
    def __init__(self, timeout):
        self._timeout = timeout

    @_inject_session
    def _get(self, session, url, headers) -> Rensponse:
        response = session.get(url=url, timeout=self._timeout, headers=headers)
        return Rensponse(response)

    # HTTP invocation
    def get(self, url, headers=None) -> Rensponse:
        return self._get(None, url, headers)

    def post(self):
        raise NotImplementedError()

    def put(self):
        raise NotImplementedError()

    def delete(self):
        raise NotImplementedError()

    def head(self):
        raise NotImplementedError()
