# -*- coding: utf-8 -*-
import logging
from squirrel.lib.db.rds import mysql

LOG = logging.getLogger(__name__)


class rds(object):

    @classmethod
    def connect(self, rds_db=mysql, *args, **kargs):
        self.rds_db = rds_db(*args, **kargs)

    @classmethod
    def update_record(self, user_id, incr_num, callback=None):
        LOG.info('update %s snum by %d' % (user_id, incr_num))
        self.rds_db.update_record_num(user_id, incr_num, callback)
