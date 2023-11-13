# -*- coding: utf-8 -*-
from json import loads as json_loads

from requests import get as requests_get

from Spoyt.exceptions import YouTubeException, YouTubeForbiddenException
from Spoyt.logger import log
from Spoyt.settings import YOUTUBE_API_KEY


class YouTubeVideo:
    def __init__(self, payload: dict) -> None:
        item: dict = payload.get('items', [{}])[0]
        snippet: dict = item.get('snippet', {})
        self.video_id: str = item.get('id', {}).get('videoId')
        self.title: str = snippet.get('title')
        self.description: str = snippet.get('description')
        self.published_date: str = snippet.get('publishTime', '')[:10]

    @property
    def video_link(self) -> str:
        return f'https://www.youtube.com/watch?v={self.video_id}'

    @property
    def video_thumbnail(self) -> str:
        return f'https://i.ytimg.com/vi/{self.video_id}/default.jpg'


def search_video(query: str) -> YouTubeVideo:
    log.info(f'Searching YouTube: "{query}"')
    yt_r = requests_get(
        'https://www.googleapis.com/youtube/v3/search'
        '?key={}'
        '&part=snippet'
        '&maxResults=1'
        '&q={}'.format(YOUTUBE_API_KEY, query)
    )
    content = json_loads(yt_r.content)
    if (error_code := yt_r.status_code) == 200:
        video = YouTubeVideo(content)
        log.info(f'Found YouTube video "{video.title}" ({video.video_link})')
    elif error_code == 403:
        log.critical(content['error']['message'])
        raise YouTubeForbiddenException
    else:
        log.error(content['error']['message'])
        raise YouTubeException
    return video
