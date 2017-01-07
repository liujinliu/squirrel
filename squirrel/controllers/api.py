# -*- coding: utf-8 -*-

from db import cache, persis


class record_db(object):

    @classmethod
    def set(self, user_id, timestamp, records):
        cache.insert(user_id, timestamp=timestamp,
                     doc=records)

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
