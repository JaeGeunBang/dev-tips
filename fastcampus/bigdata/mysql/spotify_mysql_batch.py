import sys
import requests
import base64
import json
import logging
import pymysql
import csv

client_id = "1775bfacc6cf46359d575b21f803376e"
client_secret = "024b942c681c4ef094ef567d802e2812"

host = "fastcampus.caiug7vc1qom.ap-northeast-2.rds.amazonaws.com"
port = 3306
username = "admin"
database = "production"

def main():

    ## password는 직접 입력받는다.
    password = sys.argv[1]

    try:
        conn = pymysql.connect(host, user=username, passwd=password, db=database, port=port, use_unicode=True, charset='utf8')
        cursor = conn.cursor()
    except:
        logging.error("could not connect to RDS")
        sys.exit(1)

    headers = get_headers(client_id, client_secret)

    cursor.execute("SELECT id FROM artists")
    artists = []
    for (id, ) in cursor.fetchall():
        artists.append(id)

    # 50개씩 리스트를 끊음.
    artists_batch = [artists[i: i+50] for i in range(0, len(artists), 50)]

    artist_genres = []

    # 50개씩 artists id 를  request함.
    for i in artists_batch:
        ids = ','.join(i)
        URL = "https://api.spotify.com/v1/artists/?ids={}".format(ids)

        r = requests.get(URL, headers=headers)
        raw = json.loads(r.text)

        for artist in raw['artists']:

            for genre in artist['genres']:

                artist_genres.append(
                    {
                        'artist_id': artist['id'],
                        'genre': genre
                    }
                )

    for data in artist_genres:
        insert_row(cursor, data, 'artist_genres')

    conn.commit()
    sys.exit(0)



def insert_row(cursor, data, table):
    placeholders = ', '.join(['%s'] * len(data))
    columns = ', '.join(data.keys())
    key_placeholders = ', '.join(['{0}=%s'.format(k) for k in data.keys()])
    sql = "INSERT INTO %s ( %s ) VALUES ( %s ) ON DUPLICATE KEY UPDATE %s" % (table, columns, placeholders, key_placeholders)
    cursor.execute(sql, list(data.values())*2)

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
