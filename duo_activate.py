
#!/usr/bin/env python3

import pyotp
import requests
import base64
import json
import sys


def activate_duo(duo_url):
    host = f"api-{duo_url.split('/')[2].split('-')[1]}"
    code = duo_url.split("/")[-1]

    url = 'https://{host}/push/v2/activation/{code}?customer_protocol=1'.format(host=host, code=code)
    headers = {'User-Agent': 'okhttp/2.7.5'}
    data = {'jailbroken': 'false',
            'architecture': 'armv7',
            'region': 'US',
            'app_id': 'com.duosecurity.duomobile',
            'full_disk_encryption': 'true',
            'passcode_status': 'true',
            'platform': 'Android',
            'app_version': '3.23.0',
            'app_build_number': '323001',
            'version': '8.1',
            'manufacturer': 'unknown',
            'language': 'en',
            'model': 'Pixel C',
            'security_patch_level': '2018-12-01'}

    r = requests.post(url, headers=headers, data=data)
    response = json.loads(r.text)

    try:
        secret = base64.b32encode(response['response']['hotp_secret'].encode()).decode()
    except KeyError:
        print(response)
        sys.exit(1)


    print("Printing next 5 One time passwords!")
    for i in range(5):
        print(f"{i}: {pyotp.HOTP(secret).at(i)}")
    
    # saving the token to a json file
    data = {
        "secret": secret,
        "offset": 0
    }

    with open('duo_token.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)
        
    with open('response.json', 'w') as resp:
        resp.write(r.text)


if len(sys.argv) < 2:
    print("Usage: python duo_bypass.py <duo activation url>")
    sys.exit()

activate_duo(sys.argv[1])