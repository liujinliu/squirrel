# -*- coding: utf-8 -*-

import boto3
import logging
from boto3.dynamodb.conditions import Key

LOG = logging.getLogger(__name__)


class CacheDb(object):

    def __init__(self, *args, **kargs):
        self.db = boto3.resource(
            'dynamodb', *args, **kargs)
        self.table_name = 'active_records'
        self.partition_key = 'user_id'
        self.sort_key = 'timestamp'
        try:
            self.table_create()
        except Exception as e:
            LOG.info(e, exc_info=True)
        self.record_tb = self.db.Table(self.table_name)

    def table_create(self):
        table = self.db.create_table(
            TableName='active_records',
            KeySchema=[
                {
                    'AttributeName': self.partition_key,
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': self.sort_key,
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': self.partition_key,
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': self.sort_key,
                    'AttributeType': 'N'
                },

            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1000,
                'WriteCapacityUnits': 1000
            }
        )
        table.meta.client.get_waiter('table_exists').wait(
            TableName=self.table_name)

    def insert(self, user_id, timestamp, doc):
        self.record_tb.put_item(
            Item={
                    self.partition_key: user_id,
                    self.sort_key: timestamp,
                    'doc': doc,
                }
        )

    def select(self, user_id, endtime):
        response = self.record_tb.query(
            KeyConditionExpression=Key(self.partition_key).eq(user_id) &
            Key(self.sort_key).lt(endtime))
        return response['Items'][::-1]

if __name__ == '__main__':
    dy = CacheDb(endpoint_url='http://localhost:8000')
    print(dy.select('abcdeliujinliu', 1484036749))
