import sys
import os
import boto3
import requests
import base64
import json
import logging
import pymysql
from boto3.dynamodb.conditions import Key, Attr

def main():

    try:
        dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2', endpoint_url='http://dynamodb.ap-northeast-2.amazonaws.com')
    except:
        logging.error('could not connect to dynamodb')
        sys.exit(1)

    table = dynamodb.Table('top_tracks')

    # 해당 방법은 artist_id, id를 모두 알아야 함. (key를 두개로 설정했기 때문에)
    response = table.get_item (
        Key={
            'artist_id':'0ECwFtbIWEVNwjlrfc6xoL',
            'id':'0cNwyA4Qiyr29I90ezhr0X'
        }
    )

    # query (artist_id만 알고 있을 때,).
    response = table.query (
        KeyConditionExpression=Key('artist_id').eq('0ECwFtbIWEVNwjlrfc6xoL'),
        FilterExpression=Attr('popularity').gt(80)
    )

    # scan (artist_id도 모를때)
    response = table.scan (
        FilterExpression=Attr('popularity').gt(80)
    )

    print(response['Items'])

if __name__=='__main__':
    main()
