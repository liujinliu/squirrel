# -*- coding: utf-8 -*-
import json
import logging
from squirrel.lib.db.localfile import persis_db
from squirrel.utils import MONTH_FMT, month_last
from datetime import datetime

LOG = logging.getLogger(__name__)


class persis(object):

    def connect(self, persis_db=persis_db, *args, **kargs):
        self.persis_db = persis_db(*args, **kargs)

    def insert(self, user_id, date=None, doc=None):
        if not doc or not date:
            LOG.error('doc or date invalid, can not insert')
            return False
        return self.persis_db.insert(user_id, date, json.dumps(doc))

    def select(self, user_id, endtime, top):
        value = datetime.utcfromtimestamp(endtime)
        utc_month = datetime.strftime(value, MONTH_FMT)
        ret = []
        while len(ret) < top:
            for tmp in self.persis_db.select(user_id, utc_month):
                if not tmp:
                    break
                ret.extend(json.loads(tmp))
            utc_month = month_last(utc_month)
        if len(ret) > top:
            return ret[0:top]
        return ret

persis = persis()
