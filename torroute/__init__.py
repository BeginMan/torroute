"""
tornado route decoration
    :copyright: (c) 2016 by fangpeng(@beginman.cn).
    :license: MIT, see LICENSE for more details.
"""
from tornado.web import url


class Route(object):
    _routes = {}

    def __init__(self, pattern, name=None, kwargs={}, group='.*$'):
        self.pattern = pattern
        self.name = name or pattern
        self.kwargs = kwargs
        self.group = group

    def __call__(self, handle_class):
        self.pattern = self._prune(self.group, self.pattern)
        spec = url(self.pattern, handle_class, self.kwargs, self.name)
        self._routes.setdefault(self.group, []).append(spec)
        return handle_class

    @staticmethod
    def _prune(group, pattern):
        if group != '.*$':
            if not group.startswith('/'):
                group = '/' + group
            if not group.endswith('/') and not pattern.startswith('/'):
                group += '/'

            pattern = (group + pattern).replace('//', '/')
        return pattern

    @classmethod
    def routes(cls):
        return reduce(lambda x, y: x + y, cls._routes.values()) \
            if cls._routes else []

    @classmethod
    def url_for(cls, name, *args):
        named_handlers = dict([(spec.name, spec) for spec in cls.routes()
                               if spec.name])
        if name in named_handlers:
            return named_handlers[name].reverse(*args)
        raise KeyError("%s not found in named urls" % name)

    @classmethod
    def get_handler_class(cls, url, group='.*$'):
        if not url.endswith('$'):
            url += '$'
        url = cls._prune(group, url)
        handlers_class = dict([(spec.regex.pattern, spec.handler_class)
                               for spec in cls.routes()])
        if url in handlers_class:
            return handlers_class[url]

        raise KeyError("%s not found in named urls" % url)

route = Route


