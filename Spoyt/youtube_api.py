# -*- coding: utf-8 -*-
from json import loads as json_loads
from os import getenv

import requests


def find_youtube_id(query: str) -> [bool, str]:
    yt_r = requests.get(
        'https://www.googleapis.com/youtube/v3/search'
        '?key={}'
        '&part=snippet'
        '&maxResults=1'
        '&q={}'.format(
            getenv('YOUTUBE_API_KEY'),
            query
        )
    )
    content = json_loads(yt_r.content)
    if (error_code := yt_r.status_code) == 200:
        data = content['items'][0]['id']['videoId']
    elif error_code == 403:
        data = 'Bot is not set properly.' \
               ' Ask the bot owner for further information.'
    else:
        data = content['error']['message']
    return [error_code == 200, data]
