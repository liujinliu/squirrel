# -*- coding: utf-8 -*-
import time
import json
from datetime import datetime
from squirrel.lib.db.cache.dynamodb import cache_db


class cache(object):

    def connect(self, cache_db=cache_db, *args, **kargs):
        self.cache_db = cache_db(*args, **kargs)

    def insert(self, user_id, timestamp=None, doc=None):
        if not doc:
            return
        if not timestamp:
            timestamp = time.mktime(datetime.now().timetuple())
        self.cache_db.insert(user_id, timestamp, json.dumps(doc))

    def select(self, user_id, endtime=None, top=1):
        if not endtime:
            endtime = time.mktime(datetime.now().timetuple())
        docs = self.cache_db.select(user_id, endtime)
        ret = json.loads(docs)
        if len(ret) >= top:
            return ret[0:top]
        else:
            return ret

cache = cache()
