# -*- coding: utf-8 -*-
import logging
from squirrel.lib.db.rds.mysql import mysqldb

LOG = logging.getLogger(__name__)


class rds(object):

    @classmethod
    def connect(self, rds_db=mysqldb, *args, **kargs):
        self.rds_db = rds_db(*args, **kargs)

    @classmethod
    def update_record(self, user_id, incr_num, timestamp, callback=None):
        LOG.info('update %s snum by %d , timestamp:%d'
                 % (user_id, incr_num, timestamp))
        self.rds_db.update_record_num(user_id, incr_num,
                                      timestamp, callback)
