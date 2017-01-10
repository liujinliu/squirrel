# -*- coding: utf-8 -*-
import logging
import boto3
import botocore
import StringIO

LOG = logging.getLogger(__name__)


class persis_db(object):
    def __init__(self, *args, **kargs):
        self.s3 = boto3.resource('s3')

    def bkt_exists(self, bkt):
        exists = True
        try:
            self.s3.meta.client.head_bucket(Bucket=bkt)
        except botocore.exceptions.ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                exists = False
            else:
                raise
        return exists

    def insert(self, user_id, date, doc):
        bkt, key = user_id, date
        LOG.debug('writing doc to %s:%s' % (bkt, key))
        if not self.bkt_exists(bkt):
            self.s3.create_bucket(Bucket=bkt)
        f = StringIO.StringIO(doc)
        self.s3.Object(bkt, key).put(Body=f)

    def select(self, user_id, utc_month):
        bkt = user_id
        if not self.bkt_exists(bkt):
            return []
        bucket = self.s3.Bucket(bkt)
        keys = list(map(lambda x: x.key,
                    bucket.objects.filter(Prefix=utc_month)))
        if utc_month in keys:
            f = StringIO.StringIO()
            self.s3.Bucket(bkt).put_object(Key=utc_month, Body=f)
            yield f.getvalue()
            return
        keys.sort(key=lambda x: int(x), reverse=True)
        for k in keys:
            f = StringIO.StringIO()
            self.s3.Bucket(bkt).put_object(Key=k, Body=f)
            yield f.getvalue()
