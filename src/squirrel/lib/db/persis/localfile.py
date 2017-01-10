# -*- coding: utf-8 -*-
import logging
import re
from os.path import join as path_join,\
                    exists as path_exists,\
                    isfile
from os import makedirs, listdir

LOG = logging.getLogger(__name__)


class PersisDb(object):
    def __init__(self, base_path='/home/liujinliu/working/tmpfiles',
                 *args, **kargs):
        self.base_path = base_path
        self.valuefile = 'value'

    def userid2path(self, user_id):
        path0 = re.findall(r'.{4}', user_id)
        len0, len_user_id = 4*len(path0), len(user_id)
        if len0 < len_user_id:
            path1 = user_id[len0:]
            path0.append(path1)
        return '/'.join(path0)

    def insert(self, user_id, date, doc):
        path = path_join(self.base_path,
                         self.userid2path(user_id), date)
        LOG.debug('writing doc to %s' % path)
        if path_exists(path):
            LOG.info('%s alreay exists, will not write in')
            return False
        makedirs(path)
        value_file = path_join(path, self.valuefile)
        with open(value_file, 'w') as f:
            f.write(doc)
        LOG.debug('write doc to %s success' % path)

    def select(self, user_id, utc_month):
        value_file = path_join(self.base_path,
                               self.userid2path(user_id),
                               utc_month, self.valuefile)
        if path_exists(value_file) and isfile(value_file):
            with open(value_file, 'r') as f:
                ret = f.read()
                yield ret
            return
        path = path_join(self.base_path,
                         self.userid2path(user_id), utc_month)
        if path_exists(path):
            dirs = listdir(path)
            dirs.sort(key=lambda x: int(x), reverse=True)
            for d in dirs:
                value_file = path_join(d, self.valuefile)
                if path_exists(value_file) and isfile(value_file):
                    with open(value_file, 'r') as f:
                        ret = f.read()
                        yield ret
