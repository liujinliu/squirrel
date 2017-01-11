# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from tornado import gen
from tornado.queues import Queue
from concurrent.futures import ThreadPoolExecutor
from db.cache import Cache
from db.persis import Persis
from squirrel.utils import USER_CACHE_MAX, DAY_FMT
q = Queue(maxsize=1000)
LOG = logging.getLogger(__name__)
thread_pool = ThreadPoolExecutor(4)
sync_records_thread = ThreadPoolExecutor(1)


def do_sync_records(user_id, timestamp):
    LOG.info('sync %s data to persis storage begin, timestamp:%d'
             % (user_id, timestamp))
    LOG.info('got all records of %s, timestamp:%d'
             % (user_id, timestamp))
    cache_records = Cache.select(user_id, timestamp,
                                 USER_CACHE_MAX*2)
    records = []
    list(map(lambda x: records.extend(x.get('doc', [])),
             cache_records))
    utc_date = datetime.utcfromtimestamp(timestamp)
    dt = datetime.strftime(utc_date, DAY_FMT)
    LOG.info('persis all records of %s, dt:%s'
             % (user_id, dt))
    Persis.insert(user_id, dt, records)
    LOG.info('update record in rds user_id:%s, timestamp:%d'
             % (user_id, timestamp))
    LOG.info('sync %s data to persis storage finish, timestamp:%d'
             % (user_id, timestamp))


@gen.coroutine
def sync_record_data():
    while True:
        val = yield q.get()
        user_id = val.get('user_id', '')
        timestamp = val.get('timestamp', 0)
        try:
            LOG.info('submit to sync user %s, timestamp:%d'
                     % (user_id, timestamp))
            yield sync_records_thread.submit(do_sync_records, user_id,
                                             timestamp)
        finally:
            q.task_done()


@gen.coroutine
def producer_sync_job(user_id, timestamp):
    LOG.info('add %s to worker queue, timestamp:%d'
             % (user_id, timestamp))
    yield q.put(dict(user_id=user_id, timestamp=timestamp))
