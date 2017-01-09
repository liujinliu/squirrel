# -*- coding: utf-8 -*-

import MySQLdb
import logging
import functools
from MySQLdb import OperationalError
from MySQLdb.cursors import DictCursor
# from contextlib import contextmanager

LOG = logging.getLogger(__name__)


class mysqldb(object):

    def __init__(self, host='172.17.0.2',
                 port=3306, user='root',
                 passwd='root', dbname='test',
                 *args, **kargs):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.dbname = dbname
        self.conn = self._conn()

    def __repr__(self):
        return '<mysqldb user:{0}>'.format(self.user)

    def _conn(self):
        return MySQLdb.connect(host=self.host,
                               port=self.port,
                               user=self.user,
                               passwd=self.passwd,
                               db=self.dbname,
                               use_unicode=True,
                               charset="utf8",
                               autocommit=False,
                               cursorclass=DictCursor)

    @property
    def cursor(self):
        return self.conn.cursor()

    # flake8: noqa
    def handle_connection_loss(func):
        @functools.wraps(func)
        def call(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except OperationalError as e:
                LOG.warn('{e}\nreconnecting.......'.format(e=e),
                         exc_info=True)
                self.conn = self._conn()
                return func(self, *args, **kwargs)
            except Exception as e:
                LOG.error(e, exc_info=True)
                raise
        return call

    def commit(self):
        self.conn.commit()

    def rollback(self, conn=None):
        self.conn.rollback()

    @handle_connection_loss
    def update_record_num(self, user_id, incr_num, callback=None):
        cursor = self.cursor
        sql = ('SELECT cache FROM active_records '
               'WHERE user_id="{user_id}" '
               'FOR UPDATE').format(user_id=user_id)
        try:
            cursor.execute(sql)
            ret = cursor.fetchone()
            cur_num = incr_num
            if ret:
                cur_num = ret.get('cache', 0) + incr_num
                if callback:
                    cur_num = callback(user_id, cur_num)
            sql = ('INSERT INTO active_records (user_id, cache) '
                   'VALUES ("{user_id}",{cur_num}) ON DUPLICATE KEY '
                   'UPDATE cache={cur_num}').format(user_id=user_id,
                                                    cur_num=cur_num)
            cursor.execute(sql)
            self.commit()
        except Exception as e:
            LOG.error(e, exc_info=True)
            self.rollback()
            raise

if __name__ == '__main__':
    m = mysqldb()

    def callback(user_id, cur_num):
        print(user_id, cur_num)
        return cur_num
    import time
    print('sleep for 3 s.....')
    time.sleep(3)
    m.update_record_num('abcde1233', 4, callback=callback)
