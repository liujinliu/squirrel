# -*- coding: utf-8 -*-

from db.cache import Cache
from db.persis import Persis
from db.rds import Rds
from squirrel.utils import USER_CACHE_MAX
from worker import producer_sync_job


def should_sync_cache2persis(user_id, cur_num, timestamp):
    if cur_num > USER_CACHE_MAX:
        producer_sync_job(user_id, timestamp)
        return True
    return False


class RecordDb(object):

    @classmethod
    def set(self, user_id, timestamp, records):
        Cache.insert(user_id, timestamp=timestamp,
                     doc=records)
        Rds.update_record(user_id, len(records), timestamp,
                          callback=should_sync_cache2persis)

    @classmethod
    def get(self, user_id, endtime, top):
        cache_records = Cache.select(user_id,
                                     endtime=endtime,
                                     top=top)
        ret = []
        list(map(lambda x: ret.extend(x.get('doc', [])), cache_records))
        len_cache = len(cache_records)
        if len_cache < top:
            newend = endtime
            if len_cache > 0:
                newend = cache_records[-1].get('timestamp', None)
            persis_records = Persis.select(user_id,
                                           endtime=newend,
                                           top=top-len_cache)
            ret.extend(list(map(lambda x: x.get('doc', []), persis_records)))
        return ret
