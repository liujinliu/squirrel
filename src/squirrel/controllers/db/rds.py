# -*- coding: utf-8 -*-
import logging
from squirrel.lib.db.rds.mysql import RdsDb

LOG = logging.getLogger(__name__)


class Rds(object):

    def connect(self, rds_db=RdsDb, *args, **kargs):
        self.rds_db = rds_db(*args, **kargs)

    def update_record(self, user_id, incr_num, timestamp, callback=None):
        LOG.info('update %s incr_num %d , timestamp:%d'
                 % (user_id, incr_num, timestamp))
        self.rds_db.update_record_num(user_id, incr_num,
                                      timestamp, callback)

Rds = Rds()

if __name__ == '__main__':
    Rds.connect()
    Rds.update_sync_state('abcde1233', 22, 1111111)
