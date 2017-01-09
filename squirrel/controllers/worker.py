# -*- coding: utf-8 -*-
import logging
from tornado import gen
from tornado.queues import Queue
from concurrent.futures import ThreadPoolExecutor

q = Queue(maxsize=1000)
LOG = logging.getLogger(__name__)
thread_pool = ThreadPoolExecutor(1)


def sync_records(user_id):
    print('====sync %s========' % user_id)
    yield gen.sleep(1)


@gen.coroutine
def sync_record_data():
    while True:
        user_id = yield q.get()
        try:
            LOG.info('submit to sync user %s' % user_id)
            yield thread_pool.submit(sync_records, user_id)
        finally:
            q.task_done()


@gen.coroutine
def producer_sync_job(user_id):
    LOG.info('add %s to worker queue')
    yield q.put(user_id)
