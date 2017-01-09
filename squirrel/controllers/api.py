# -*- coding: utf-8 -*-

from db.cache import cache
from db.persis import persis
from db.rds import rds
from squirrel.utils import USER_CACHE_MAX
from worker import producer_sync_job


def check_cached_record(user_id, cur_num):
    if cur_num > USER_CACHE_MAX:
        producer_sync_job(user_id)
        return 0
    return cur_num


class record_db(object):

    @classmethod
    def set(self, user_id, timestamp, records):
        cache.insert(user_id, timestamp=timestamp,
                     doc=records)
        rds.update_record(user_id, len(records),
                          callback=check_cached_record)

    @classmethod
    def get(self, user_id, endtime, top):
        cache_records = cache.select(user_id,
                                     endtime=endtime,
                                     top=top)
        len_cache = len(cache_records)
        if len_cache < top:
            newend = endtime
            if len_cache > 0:
                newend = cache_records[-1].get('timestamp', None)
            persis_records = persis.select(user_id,
                                           endtime=newend,
                                           top=top-len_cache)
            cache_records.extend(persis_records)
        return cache_records
