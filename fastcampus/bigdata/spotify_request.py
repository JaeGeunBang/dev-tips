import sys
import requests
import base64
import json
import logging

client_id = "1775bfacc6cf46359d575b21f803376e"
client_secret = "024b942c681c4ef094ef567d802e2812"

def main():
    headers = get_headers(client_id, client_secret)

    params = {
        "q":"BTS",
        "type":"artist",
        "limit":"5"
    }

    # 에러 핸들링
    try:
        # 받은 access_token을 header에 넣고, paramerter와 같이 특정 Endpoint에 GET을 요청한다.
        r = requests.get("https://api.spotify.com/v1/search", params=params, headers=headers)

        # 정상 코드가 아니라면
        if r.status_code != 200:
            logging.error(json.loads(r.text))

            # 429라면, 좀 쉬었다가 다시 전송 (너무 많이 보냈다는 의미.)
            if r.status_code == 429:
                # Retry_After 정보를 가져와, 해당 시간 만큼 sleep 함.
                retry_after = json.loads(r.headers)['Retry-After']
                time.sleep(int(retry_after))

                r = requests.get("https://api.spotify.com/v1/search", params=params, headers=headers)

            # 401라면, access_token이 만료되었음.
            elif r.status_code == 401:
                headers = get_headers(client_id, client_secret)
                r = requests.get("https://api.spotify.com/v1/search", params=params, headers=headers)
            else:
                sys.exit(1)
    except:
        logging.error(r.text)
        sys.exit(1)

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
