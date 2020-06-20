import copy
import json
import os
from pathlib import Path

import pandas as pd
import yaml


class Loader:
    @staticmethod
    def load(path):
        pass


class FileLoader(Loader):
    @staticmethod
    def load(path):
        with open(path, 'r') as f:
            try:
                return f.read()
            except Exception as e:
                print(e)
                raise e


class YamlLoader(Loader):
    @staticmethod
    def load(path):
        with open(path, 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)


class CSVLoader(Loader):
    @staticmethod
    def load(path):
        return pd.read_csv(path, index_col=0).Webpage


class TextLoader:
    @staticmethod
    def get_url_list(path):
        with open(path, 'r') as f:
            return f.read().splitlines()


class JSONLoader:
    @staticmethod
    def get_url_list(path):
        df = pd.read_json(path)
        return df["url"].tolist()

    @staticmethod
    def get_url_iterator(path, col=None):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if None is col:
                    yield json.loads(line)
                else:
                    yield json.loads(line)[col]


class Folder:
    @staticmethod
    def safe_create(path):
        Path(path).mkdir(parents=True, exist_ok=True)

    class PathBuilder:
        def __init__(self):
            self._hierarchy = []
            self._file_name = None

        def append_path(self, path):
            if None is path:
                return self
            self._hierarchy.append(path)
            return self

        def set_file_name(self, file_name):
            self._file_name = file_name
            return self

        def build_path(self):
            path = os.path.join(*tuple(self._hierarchy))
            if None is not self._file_name:
                return os.path.join(path, self._file_name)
            else:
                return path

        def __deepcopy__(self, memodict={}):
            cls = self.__class__
            result = cls.__new__(cls)
            memodict[id(self)] = result
            for k, v in self.__dict__.items():
                setattr(result, k, copy.deepcopy(v, memodict))
            return result
