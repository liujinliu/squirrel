# -*- coding: utf-8 -*-

from handlers.index import Root, Ping
from handlers.records import RecordHandler

urls = [
    (r"/", Root),
    (r"/ping", Ping),
    (r"/v1/record", RecordHandler),
]
