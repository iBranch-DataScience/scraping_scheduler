import threading

from singleton_decorator import singleton


@singleton
class Counter:
    def __init__(self):
        self._mutex = threading.Lock()
        self._cnt = 0

    def count(self):
        try:
            self._mutex.acquire(blocking=True)
            self._cnt = self._cnt + 1
            value = self._cnt
        finally:
            self._mutex.release()
        return value
