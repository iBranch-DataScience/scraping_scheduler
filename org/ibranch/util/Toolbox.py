import base64
import json
import math
import numbers
from datetime import datetime


class JSON:
    @staticmethod
    def build(data):
        return json.dumps(data, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Formatter:
    @staticmethod
    def get_timestamp(format="%Y%m%d_%H%M%S"):
        return str((datetime.now().strftime(format)))

    @staticmethod
    def to_lower_case_dict(pair):
        return dict((k.lower(), v.lower()) for k, v in pair.items())


class Cryptor:
    @staticmethod
    def encode(target):
        b = base64.b64encode(f'sscd={target}'.encode("utf-8"))
        return str(b, "utf-8")

    @staticmethod
    def decode(target):
        return str(base64.b64decode(target), "utf-8")[5:]


class CollectionUtil:
    @staticmethod
    def split(target, n_unit):
        if not len(target):
            return target
        split_list = range(0, len(target), n_unit)
        split_list = list(split_list)
        del split_list[0]
        return [target[i: j] for i, j in zip([0] + split_list, split_list + [None])]


class LogicUtil:
    @staticmethod
    def if_else_default(origin, fallback, func_type_check = None):
        if None is origin:
            return fallback
        if None is not func_type_check and not func_type_check(origin):
            return fallback
        if isinstance(origin, numbers.Number) and math.isnan(origin):
            return fallback
        if isinstance(origin, str) and len(origin.strip()) == 0:
            return fallback
        return origin

    @staticmethod
    def safe_get_key(d: dict, key: str):
        if key in d.keys():
            return d[key]
        return None