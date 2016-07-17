# -*-coding:utf-8-*-
from www import config_default


# 检查配置文件是否为字典
def merge(defaults, override):
    r = {}
    for k, v in defaults.items():
        if k in override:
            if isinstance(v, dict):
                r[k] = merge(r, override)
            else:
                r[k] = override[k]
        else:
            r[k] = v
    return r


class Dict(dict):
    '''
    Simple dict support access as x.y style
    '''

    def __init__(self, name=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(name, values):
            self[k] = v

        def __getattr__(self, key):
            try:
                return self[key]
            except KeyError:
                raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

        def __setattr__(self, key, value):
            self[key] = value


def toDict(d):
    D = Dict()
    for k, v in d.items():
        D[k] = toDict(v) if isinstance(v, dict) else v
    return D


configs = config_default.configs
try:
    from www import config_override

    configs = merge(configs, config_override.configs)
except ImportError:
    pass
configs = toDict(configs)
