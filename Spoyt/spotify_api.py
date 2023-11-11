# -*- coding: utf-8 -*-
from os import getenv

from spotipy import Spotify, SpotifyClientCredentials

from Spoyt.logging import log


class Track:
    def __init__(self, payload: dict) -> None:
        self.name: str = payload.get('name')
        self.track_id: str = payload.get('id')
        self.artists: list[str] = list(map(
            lambda a: a.get('name'),
            payload.get('artists', {})
        ))
        self.release_date: str = payload.get('album', {}).get('release_date')
        self.cover_url: str = payload.get('album', {}).get('images', [{}])[0].get('url')

    @property
    def is_single_artist(self) -> bool:
        return len(self.artists) == 1

    @property
    def track_url(self) -> str:
        return f'https://open.spotify.com/track/{self.track_id}'

class Playlist:
    def __init__(self, payload: dict) -> None:
        self.name: str = payload.get('name')
        self.description: str = payload.get('description')
        self.playlist_id: str = payload.get('id')
        self.owner_name: str = payload.get('owner', {}).get('display_name')
        self.owner_id: str = payload.get('owner', {}).get('id')
        self.cover_url: str = payload.get('images', [{}])[0].get('url')
        self.tracks: list[Track] = list(map(
            lambda a: Track(a.get('track', {})),
            payload.get('tracks', {}).get('items')
        ))
        self.total_tracks: int = payload.get('tracks', {}).get('total')
        self.query_limit: int = payload.get('tracks', {}).get('limit')

    @property
    def playlist_url(self) -> str:
        return f'https://open.spotify.com/playlist/{self.playlist_id}'

    @property
    def owner_url(self) -> str:
        return f'https://open.spotify.com/user/{self.owner_id}'

    @property
    def is_query_limited(self) -> bool:
        return len(self.tracks) == self.query_limit


def spotify_connect() -> Spotify:
    return Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=getenv('SPOTIFY_CLIENT_ID'),
            client_secret=getenv('SPOTIFY_CLIENT_SECRET')
        )
    )

# Search functions should not return `class Track` or `class Playlist`
# because of checks if connections was successful during runtime.

def search_track(track_id: str) -> dict:
    log.info(f'Searching track by ID "{track_id}"')
    return spotify_connect().track(track_id=track_id)


def search_playlist(playlist_id: str) -> dict:
    log.info(f'Searching playlist by ID "{playlist_id}"')
    return spotify_connect().playlist(playlist_id=playlist_id)
