import os
import argparse
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')
BASE_URL = 'https://api-ssl.bitly.com/v4/'
HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}


def create_bitlink(long_link):
    payload = {
        'long_url': long_link
    }
    url = BASE_URL + 'bitlinks'
    response = requests.post(url, headers=HEADERS, json=payload)
    if response.ok:
        return response.json()['link']


def get_info(bitlink):
    url = BASE_URL + f'bitlinks/{bitlink}'
    response = requests.get(url, headers=HEADERS)
    if response.ok:
        return response.json()['link']


def get_clicks(link):
    payload = {
        'unit': 'day',
        'units': '-1'
    }
    url = BASE_URL + f'bitlinks/{bitlink}/clicks'
    response = requests.get(url, headers=HEADERS, params=payload)
    if response.ok:
        clicks = []
        for day in response.json()['link_clicks']:
            date = datetime.strptime(day['date'], '%Y-%m-%dT%H:%M:%S%z')
            clicks.append((date.strftime('%Y-%m-%d'), day['clicks']))
        return clicks


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Программа сокращает длинные ссылки и показывает статистику переходов'
    )
    parser.add_argument('link', help='Длинная ссылка для сокращения или короткая для получения статистики')
    args = parser.parse_args()
    link = args.link

    bitlink = link.replace('http://', '').replace('https://', '')
    bitlink_info = get_info(bitlink)

    result = get_clicks(bitlink) if bitlink_info is not None else create_bitlink(link)

    if result is None:
        result = 'Убедитесь что ссылка корректна. При сокращении произошла ошибка'

    print(result)
