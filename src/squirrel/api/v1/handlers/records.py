# -*- coding: utf-8 -*-
import time
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from tornado.gen import coroutine, Return
from base import BaseHandler
from err_code import INVALID_PARA
from squirrel.controllers.api import RecordDb

LOG = logging.getLogger(__name__)
thread_pool = ThreadPoolExecutor(8)


class RecordHandler(BaseHandler):

    def get_json(self):
        if not self.json_args:
            return False
        self.user_id = self.json_args.get('user_id', '')
        self.timestamp = self.json_args.get(
            'timestamp', 0)
        self.records = self.json_args.get('records', [])
        if self.user_id and self.timestamp and self.records:
            return True
        else:
            return False

    @coroutine
    def put(self):
        if not self.get_json():
            self.write(dict(code=INVALID_PARA,
                            msg='parameters invalid'))
            raise Return(0)
        LOG.info(('parameters:\nuser_id:{user_id}\n'
                  'timestamp:{timestamp}\nrecords:{records}').format(
                      user_id=self.user_id, timestamp=self.timestamp,
                      records=self.records
                  ))
        yield thread_pool.submit(RecordDb.set, self.user_id,
                                 int(self.timestamp), self.records)

    @coroutine
    def get(self):
        self.user_id = self.get_argument('user_id', '')
        self.top = self.get_argument('top', 1)
        self.endtime = self.get_argument('endtime',
                                         time.mktime(
                                             datetime.now().timetuple()))
        if not self.user_id:
            self.write(dict(code=INVALID_PARA,
                            msg='parameters invalid'))
            return
        LOG.info(('parameters:\nuser_id:{user_id}\n'
                  'endtime:{endtime}\ntop:{top}').format(
                      user_id=self.user_id, endtime=self.endtime,
                      top=self.top
                  ))
        ret = yield thread_pool.submit(RecordDb.get, self.user_id,
                                       int(self.endtime), int(self.top))
        self.write(dict(records=ret))
