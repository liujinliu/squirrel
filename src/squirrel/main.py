# -*- coding: utf-8 -*-

from tornado.options import define, options
from controllers.db.cache import cache
from controllers.db.persis import persis
from controllers.db.rds import rds
from controllers.worker import sync_record_data
define('port', default=9999, type=int, help='app listen port')
define('debug', default=False, help='debug option')


def main():
    options.parse_command_line()
    from api.v1.urls import urls
    from tornado.web import Application
    import tornado.ioloop
    app = Application(urls, debug=options.debug)
    app.listen(options.port)
    ioloop = tornado.ioloop.IOLoop.instance()
    cache.connect(endpoint_url='http://localhost:8000')
    persis.connect()
    rds.connect()
    ioloop.spawn_callback(sync_record_data)
    ioloop.start()

if __name__ == '__main__':
    main()
