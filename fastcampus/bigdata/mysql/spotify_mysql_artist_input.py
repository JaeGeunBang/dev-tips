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

    ## artists 리스트를 읽어 artists list에 저장한다.
    artists = []
    with open('artist_list.csv') as f:
        raw = csv.reader(f)
        for row in raw:
            artists.append(row[0])

    for a in artists:
        params = {
            "q": a,
            "type": "artist",
            "limit": "1"
        }

        r = requests.get("https://api.spotify.com/v1/search", params=params, headers=headers)

        raw = json.loads(r.text)

        artist = {}
        try:
            artist_raw = raw['artists']['items'][0]
            if artist_raw['name'] == params['q']:

                artist.update(
                    {
                        'id': artist_raw['id'],
                        'name': artist_raw['name'],
                        'followers': artist_raw['followers']['total'],
                        'popularity': artist_raw['popularity'],
                        'url': artist_raw['external_urls']['spotify'],
                        'image_url': artist_raw['images'][0]['url']
                    }
                )
                insert_row(cursor, artist, 'artists')
        except:
            logging.error('something worng')
            continue

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
