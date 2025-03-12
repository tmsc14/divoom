import os
import requests
import json
import csv
from flask import abort

from datetime import datetime
from pathlib import Path

script_name = os.environ.get('SCRIPT_NAME', '') # NOTE: WSGI-conform base-path/url-prefix
divoom_api_url = 'https://app.divoom-gz.com'

def parse_bool_value(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {'true', 'yes', '1'}
    else:
        raise ValueError(f'expected bool or string; got {type(value)}')


def get_swagger_config():
    return {
        'title': 'Pixoo REST',
        'version': Path('version.txt').read_text(),
        'description': 'A RESTful API to easily interact with the Wi-Fi enabled {} devices.'.format(
            '<a href="https://www.divoom.com/de/products/pixoo-64">Divoom Pixoo</a>'
        ),
        'termsOfService': '',
        'basePath': script_name,
        'url_prefix': script_name
    }


def get_additional_swagger_template():
    return {
        'tags': [
            {
                'name': 'draw',
                'description': 'draw lines, pixels, rectangles, etc. on your Pixoo'
            },
            {
                'name': 'send',
                'description': 'send text, GIFs, etc. to your Pixoo'
            },
            {
                'name': 'set',
                'description': 'set brightness, channel, clock, etc. on your Pixoo'
            },
            {
                'name': 'pass-through',
                'description': "directly pass commands to your Pixoo's built-in HTTP-API"
            },
            {
                'name': 'divoom',
                'description': f'send requests to the external vendor API ({divoom_api_url})'
            },
            {
                'name': 'download',
                'description': 'automatically download and send resources to your Pixoo'
            }
        ]
    }


def try_to_request(url):
    try:
        print(f'[{(datetime.now().strftime("%Y-%m-%d %H:%M:%S %z").strip())}] Trying to request "{url}" ... ', end='')

        if requests.get(url).status_code == 200:
            print('OK.')
            return True
    except:
        print('FAILED.')
        return False


def divoom_api_call(endpoint, payload=None):
    return requests.post(
        f'{divoom_api_url}/{endpoint}',
        json.dumps(payload)
    )
    
def read_kpis():
    try:
        if not os.path.exists('data/kpis.csv'):
            abort(404, "KPIs file not found")
            
        with open('data/kpis.csv', 'r') as f:
            reader = csv.DictReader(f)
            required_columns = ['id','name','value','icon','position_x','position_y']
            
            if not all(col in reader.fieldnames for col in required_columns):
                abort(400, "CSV missing required columns")
                
            return list(reader)
            
    except Exception as e:
        abort(500, f"Error reading KPIs: {str(e)}")