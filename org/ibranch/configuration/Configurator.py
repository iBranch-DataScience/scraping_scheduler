import logging
import logging.config

import config_with_yaml as config
from singleton_decorator import singleton

from org.ibranch.util.Toolbox import LogicUtil


def check_initialization(func):
    def _check_initialization(*args, **kwargs):
        self = args[0]
        if self._cfg is None:
            raise SystemExit('Configuration not initialized')
        return func(*args, **kwargs)
    return _check_initialization


@singleton
class Configuration:
    def __init__(self):
        self._path = "resource/property/properties.yaml"
        self.ad_hoc_properties = dict()


    def _init_logging(self):
        path = self.getProperty('logger.path')
        level = self.getProperty('logger.level')
        level = logging.getLevelName(level)
        logging.config.fileConfig(path)
        logging.getLogger().setLevel(level)

    def _init_config(self):
        self._cfg = config.load(self._path)

    def file_path(self, path: str):
        if None is path or len(path.strip()) == 0:
            raise SystemError('Configuration path is invalid!')
        self._path = path
        return self

    def initialize(self):
        self._init_config()
        self._init_logging()
        return self

    @check_initialization
    def getProperty(self, prop: str):
        return LogicUtil.if_else_default(
            LogicUtil.safe_get_key(self.ad_hoc_properties, prop),
            self._cfg.getProperty(prop)
        )

    @check_initialization
    def getPropertyWithDefault(self, prop: str, default: str):
        return LogicUtil.if_else_default(
            LogicUtil.safe_get_key(self.ad_hoc_properties, prop),
            self._cfg.getPropertyWithDefault(prop, default)
        )

    def replace_property(self, key, value):
        self.ad_hoc_properties[key] = value
        return self
