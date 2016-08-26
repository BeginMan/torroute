# torroute

Tornado Route.

# Installation:

    pip install torroute

# Usage:

```python
import tornado.ioloop
import tornado.web

from toroute import route

@route('/')
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

@route('/login', name='login')
class LoginHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write('login')

# group by `/blog`, e.g.: blog app
@route('/list', name='blog_list', kwargs={'data': 'hello'}, group='/blog')
class BlogListHandler(tornado.web.RequestHandler):
    def initialize(self, **kwargs):
        self.data = kwargs.get('data', None)

    def get(self, *args, **kwargs):
        self.write(self.data)

@route('/post', name='blog_post', group='/blog')
class BlogPostHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        print('post complete! redirect:%s' % route.url_for('blog_list'))
        self.redirect(route.url_for('blog_list'))

@route(r'/view/(?P<pid>\d+)/detail', name='blog_view', group='/blog')
class BlogViewHandler(tornado.web.RequestHandler):
    def get(self, pid, **kwargs):
        msg = 'Handle Class for /blog/list is %s' \
              % route.get_handler_class('/list', group='/blog').__name__
        self.write(msg)

if __name__ == '__main__':

    application = tornado.web.Application([
        (r"/", MainHandler),
    ] + route.routes())
    application.listen(8000)
    tornado.ioloop.IOLoop.current().start()

```