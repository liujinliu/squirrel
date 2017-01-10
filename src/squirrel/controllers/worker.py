# -*- coding: utf-8 -*-
import logging
from tornado import gen
from tornado.queues import Queue
from concurrent.futures import ThreadPoolExecutor

q = Queue(maxsize=1000)
LOG = logging.getLogger(__name__)
thread_pool = ThreadPoolExecutor(1)


@gen.coroutine
def sync_records(user_id, timestamp):
    LOG.info('sync %s data to persis storage begin, timestamp:%d'
             % (user_id, timestamp))
    yield gen.sleep(1)
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
            yield thread_pool.submit(sync_records, user_id,
                                     timestamp)
        finally:
            q.task_done()


@gen.coroutine
def producer_sync_job(user_id, timestamp):
    LOG.info('add %s to worker queue, timestamp:%d'
             % (user_id, timestamp))
    yield q.put(dict(user_id=user_id, timestamp=timestamp))
