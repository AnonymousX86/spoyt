# -*- coding: utf-8 -*-
from os import getenv

import google_auth_oauthlib.flow
import googleapiclient.discovery


def create_youtube() -> googleapiclient.discovery:
    flow = google_auth_oauthlib.flow.InstalledAppFlow. \
                from_client_secrets_file(
                    getenv('YOUTUBE_CLIENT_SECRET_FILE'),
                    ['https://www.googleapis.com/auth/youtube.force-ssl']
                )
    credentials = flow.run_local_server()
    youtube = googleapiclient.discovery.build(
        'youtube',
        'v3',
        credentials=credentials
    )
    return youtube


def search_youtube(youtube: googleapiclient.discovery, query: str) -> str:
    yt_req = youtube.search().list(
        part='snippet',
        maxResults=1,
        q=query,
        type='video'
    )
    yt_res = yt_req.execute()
    return yt_res['items'][0]['id']['videoId']
