# -*- coding: utf-8 -*-
from os import getenv

from spotipy import Spotify, SpotifyClientCredentials

from Spoyt.logging import log


class Track:
    def __init__(
            self,
            name: str,
            track_id: str,
            artists: list[str],
            release_date: str,
            album_url: str
    ):
        self.name: str = name
        self.track_id: str = track_id
        self.artists: list[str] = artists
        self.release_date: str = release_date
        self.album_url: str = album_url

    @property
    def is_single_artist(self):
        return len(self.artists) == 1

    @property
    def track_url(self):
        return f'https://open.spotify.com/track/{self.track_id}'


def model_track(track: dict) -> Track:
    return Track(
        name=track['name'],
        track_id=track['id'],
        artists=list(map(lambda a: a['name'], track['artists'])),
        release_date=track['album']['release_date'],
        album_url=track['album']['images'][0]['url']
    )


def search_spotify(track_id: str) -> dict:
    log.info(f'Searching ID "{track_id}"')
    spotify = Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=getenv('SPOTIFY_CLIENT_ID'),
            client_secret=getenv('SPOTIFY_CLIENT_SECRET')
        )
    )
    return spotify.track(track_id=track_id)
