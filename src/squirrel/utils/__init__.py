# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

USER_CACHE_MAX = 10
MONTH_FMT = '%Y/%m'
DAY_FMT = '%Y/%m/%d'


def month_last(month_str):
    day_str = '%s/10' % month_str
    dt = datetime.strptime(day_str, DAY_FMT)
    new_dt = dt + timedelta(days=-20)
    return datetime.strftime(new_dt, MONTH_FMT)
