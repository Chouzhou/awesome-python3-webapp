# -*-coding:utf-8 -*-
import functools

# 定义get
import asyncio
import inspect
import logging
import os


def get(path):
    '''

    Define decorator @get('/path')
    '''

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)

        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return wrapper

    return decorator


# 定义post
def post(path):
    '''
    Define decorator @post('/path
    '''

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)

        wrapper.__method__ = 'POST'
        wrapper.__route__ = path
        return wrapper

    return decorator


# 获取可得的关键词
def get_required_kw_args(fn):
    args = []
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        # 判断关键词 默认值
        if param.kind == inspect.Parameter.KEYWORD_ONLY and param.default == inspect.Parameter.empty:
            args.append(name)
    return tuple(args)


def get_named_kw_args(fn):
    args = []
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            args.append(name)
    return tuple(args)


# 判断命名关键词是否正确
def has_named_kw_args(fn):
    # args = []
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            # args.append(name)
            return True


# 判断关键词种类
def has_var_kw_arg(fn):
    # args = []
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            # args.append(name)
            return True


# 判断是否有请求
def has_request_arg(fn):
    sig = inspect.signature(fn)
    params = sig.parameters
    found = False
    for name, param in params.items():
        if found and (param.kind != inspect.Parameter.KEYWORD_ONLY and
                              param.kind != inspect.Parameter.VAR_POSITIONAL and
                              param.kind != inspect.Parameter.VAR_KEYWORD
                      ):
            raise ValueError('request paramter must be the last named parameter in function:%s%s') % (
                fn.__name__, str(sig))
    return found


class RequestHandle(object):
    def __init__(self, app, fn):
        self.app = app
        self._func = fn
        # 还有补充的内容

    async def __call__(self, request):
        # 还有其他的东西
        kw = None
        r = await self._func(**kw)
        return r


# 处理URL函数
def add_route(app, fn):
    method = getattr(fn, '__method__', None)
    path = getattr(fn, '__route__', None)
    if path is None or method is None:
        raise ValueError('@get or @post not defined in %s.' % str(fn))
    if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
        fn = asyncio.coroutine(fn)
    logging.info(
            'add route %s %s => %s(%s)' % (
                method, path, fn.___name__, ','.join(inspect.signature(fn).parameters.keys())))
    app.router.add_route(method, path, RequestHandle(app, fn))


# 自动扫描
def add_routes(app, module_name):
    n = module_name.rfind('.')
    if n == (-1):
        mod = __import__(module_name, globals(), locals())
    else:
        name = module_name[n + 1:]
        mod = getattr(__import__(module_name[:n], globals(), locals(), [name]), name)
    for attr in dir(mod):
        if attr.startswith('_'):
            continue
        fn = getattr(mod, attr)
        # callable检查函数是否能使用
        if callable(fn):
            method = getattr(fn, '__method__', None)
            path = getattr(fn, '__route__', None)
            if method and path:
                add_route(app, fn)


# 添加静态资源文件夹路径
def add_static(app):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    app.router.add_static('/static/', path)
    logging.info('add static %s => %s' % ('/static/', path))
