import logging
import logging.config
import os

import config_with_yaml as config
from singleton_decorator import singleton

from scraping_scheduler.ibranch.util.Toolbox import LogicUtil


def check_initialization(func):
    def _check_initialization(*args, **kwargs):
        self = args[0]
        if self._cfg is None:
            raise SystemExit('Configuration not initialized')
        return func(*args, **kwargs)
    return _check_initialization


@singleton
class Configuration:
    def __init__(self, args):
        self._root_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        self._path = os.path.join(self._root_dir, "resource/property/properties.yaml")
        self.ad_hoc_properties = dict()
        self._cfg = None
        self._init_config()
        self._init_logging()
        self._init_args(args)

    def _init_args(self, args):
        if not args or len(args) == 0:
            return
        ad_hoc_cfg = dict()
        key, values = None, list()
        for item in args:

            if item.startswith('-'):
                ## Add value to previous key
                if None is not key:
                    ad_hoc_cfg[key] = values.copy()

                ## Create new key
                values.clear()
                key = item.replace('-', '')
            else:
                values.append(item)
        ad_hoc_cfg[key] = values

        for key, values in ad_hoc_cfg.items():
            value = values
            if len(value) == 0:
                value = ''
            elif len(value) == 1:
                value = value[0]
            self.replace_property(key, value)

        path = self.getPropertyWithDefault('cfg_path', None)

        if path:
            self.file_path(path)
            self._init_config()
            self._init_logging()

    def _init_logging(self):
        path = self.getProperty('logger.path')
        level = self.getProperty('logger.level')
        level = logging.getLevelName(level)
        try:
            logging.config.fileConfig(os.path.abspath(path))
        except:
            logging.config.fileConfig(os.path.join(self._root_dir, path))
        logging.getLogger().setLevel(level)

    def _init_config(self):
        cfg = config.load(self._path)
        if not self._cfg:
            self._cfg = cfg
            return
        self._override_cfg(self._cfg.getNode(), cfg.getNode())

    def _override_cfg(self, old, new):
        for k, v in new.items():
            if not isinstance(v, dict):
                old[k] = v
                continue
            if k not in old:
                old[k] = dict()
            self._override_cfg(old[k], new[k])

    def file_path(self, path: str):
        if None is path or len(path.strip()) == 0:
            raise SystemError('Configuration path is invalid!')
        self._path = path
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
