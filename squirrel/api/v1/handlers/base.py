# -*- coding: utf-8 -*-
import json
from tornado.web import RequestHandler


class BaseHandler(RequestHandler):

    def prepare(self):
        if self.request.headers['Content-Type'].startswith('application/json'):
            self.json_args = json.loads(self.request.body, encoding='utf-8')
        else:
            self.json_args = None
