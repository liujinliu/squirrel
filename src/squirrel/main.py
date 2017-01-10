# -*- coding: utf-8 -*-

from tornado.options import define, options
from controllers.db.cache import Cache
from controllers.db.persis import Persis
from controllers.db.rds import Rds
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
    Cache.connect(endpoint_url='http://localhost:8000')
    Persis.connect()
    Rds.connect()
    ioloop.spawn_callback(sync_record_data)
    ioloop.start()

if __name__ == '__main__':
    main()
