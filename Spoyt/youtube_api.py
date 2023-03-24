# -*- coding: utf-8 -*-
from json import loads as json_loads
from os import getenv

import requests

from Spoyt.logging import log


class YouTubeResult:
    def __init__(
            self, 
            found: bool, 
            id: str = None, 
            title: str = None,
            description: str = None,
            published_date: str = None
    ) -> None:
        self.found = found
        self.id = id
        self.title = title
        self.description = description
        self.published_date = published_date

    @property
    def video_link(self) -> str:
        return f'https://www.youtube.com/watch?v={self.id}'
    
    @property
    def video_thumbnail(self) -> str:
        return f'https://i.ytimg.com/vi/{self.id}/default.jpg'


def find_video_by_id(query: str) -> YouTubeResult:
    log.info(f'Searching YouTube: "{query}"')
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
        data = YouTubeResult(
            found=True,
            id=content['items'][0]['id']['videoId'],
            title=content['items'][0]['snippet']['title'],
            description=content['items'][0]['snippet']['description'],
            published_date=content['items'][0]['snippet']['publishTime'][:10]
        )
        log.info(f'Found YouTube video "{data.title}" ({data.video_link})')
    elif error_code == 403:
        data = YouTubeResult(
            found=False,
            description='Bot is not set properly. Ask the bot owner for further information.'
        )
        log.error(content['error']['message'])
    else:
        data = YouTubeResult(
            found=False,
            description=content['error']['message']
        )
        log.error(content['error']['message'])
    return data
