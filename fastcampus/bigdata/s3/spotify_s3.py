import sys
import os
import boto3
import requests
import base64
import json
import logging
import pymysql
from datetime import datetime
import pandas as pd
import jsonpath

client_id = "1775bfacc6cf46359d575b21f803376e"
client_secret = "024b942c681c4ef094ef567d802e2812"

host = "fastcampus.caiug7vc1qom.ap-northeast-2.rds.amazonaws.com"
port = 3306
username = "admin"
database = "production"

# RDS - 아티스트 id를 가져온다.
## 해당 id를 통해 Spority API를 통해 데이터를 가져온다.
## 불러온 데이터를 .json 형태로 저장해서 S3에 저장할 것.

def main():

    password = sys.argv[1]

    try:
        conn = pymysql.connect(host, user=username, passwd=password, db=database, port=port, use_unicode=True, charset='utf8')
        cursor = conn.cursor()
    except:
        logging.error("could not connect to rds")
        sys.exit(1)

    headers = get_headers(client_id, client_secret)

    # RDS - 아티스트 ID를 가져오고
    cursor.execute("SELECT id FROM artists LIMIT 10")

    top_track_keys = {
        "id": "id",
        "name": "name",
        "popularity": "popularity",
        "external_url": "external_urls.spotify"
    }
    # Top Tracks Spotify 가져오고
    top_tracks = []
    for (id, ) in cursor.fetchall():

        URL = "https://api.spotify.com/v1/artists/{}/top-tracks".format(id)
        params = {
            'country': 'US'
        }
        r = requests.get(URL, params=params, headers=headers)
        raw = json.loads(r.text)

        for i in raw['tracks']:
            top_track = {}
            for k, v in top_track_keys.items():
                top_track.update({k: jsonpath.jsonpath(i, v)})
                top_track.update({'artist_id': id})
                top_tracks.append(top_track)

    # track_ids
    track_ids = [i['id'][0] for i in top_tracks]

    top_tracks = pd.DataFrame(top_tracks)
    top_tracks.to_parquet('top-tracks.parquet', engine='pyarrow', compression='snappy')

    dt = datetime.utcnow().strftime("%Y-%m-%d")

    s3 = boto3.resource('s3')
    object = s3.Object('spotify-artists-1', 'top-tracks/dt={}/top-tracks.parquet'.format(dt))
    data = open('top-tracks.parquet', 'rb')
    object.put(Body=data)
    # S3 import

    tracks_batch = [track_ids[i: i+100] for i in range(0, len(track_ids), 100)]

    audio_features = []
    for i in tracks_batch:

        ids = ','.join(i)
        URL = "https://api.spotify.com/v1/audio-features/?ids={}".format(ids)

        r = requests.get(URL, headers=headers)
        raw = json.loads(r.text)

        audio_features.extend(raw['audio_features'])

    audio_features = pd.DataFrame(audio_features)
    audio_features.to_parquet('audio-features.parquet', engine='pyarrow', compression='snappy')

    s3 = boto3.resource('s3')
    object = s3.Object('spotify-artists-1', 'audio-features/dt={}/top-tracks.parquet'.format(dt))
    data = open('audio-features.parquet', 'rb')
    object.put(Body=data)



def get_headers(client_id, client_secret):
    endpoint = "https://accounts.spotify.com/api/token"
    encoded = base64.b64encode("{}:{}".format(client_id, client_secret).encode('utf-8')).decode('ascii')

    headers = {
        "Authorization": "Basic {}".format(encoded)
    }

    payload = {
        "grant_type": "client_credentials"
    }

    # post를 통해 access_token을 받아온다.
    r = requests.post(endpoint, data=payload, headers=headers)
    access_token = json.loads(r.text)['access_token']

    # curl -H "Authorization": "Bearer NDIWWH#... (헤더 형태)"
    headers = {
        "Authorization": "Bearer {}".format(access_token)
    }

    return headers

if __name__=='__main__':
    main()
