# -*- coding: utf-8 -*-
from os import getenv

from discord import Embed, Color, Member
from spotipy import Spotify, SpotifyClientCredentials


class Track:
    def __init__(
            self,
            name: str,
            track_id: str,
            artists: str or list[str],
            release_date: str,
            album_url: str
    ):
        self.name = name
        self.track_id = track_id
        self.artists = artists
        self.release_date = release_date
        self.album_url = album_url

    @property
    def is_single_artist(self):
        return len(self.artists) == 1

    @property
    def track_url(self):
        return f'https://open.spotify.com/track/{self.track_id}'


class TrackEmbed(Embed):
    def __init__(self, track: Track):
        super().__init__()
        self.title = track.name
        self.description = f'<{track.track_url}>'
        self.color = Color.green()
        self.add_field(
            name='Artist{}'.format(
                '' if track.is_single_artist else 's'),
            value=', '.join(track.artists),
            inline=track.is_single_artist
        ).add_field(
            name='Released',
            value=track.release_date
        ).set_thumbnail(
            url=track.album_url
        )

    def add_author(self, author: Member):
        self.set_author(
            name=f'{author.display_name} shared:',
            icon_url=author.display_avatar.url
        )


def model_track(track: dict) -> Track:
    return Track(
        name=track['name'],
        track_id=track['id'],
        artists=list(map(lambda a: a['name'], track['artists'])),
        release_date=track['album']['release_date'],
        album_url=track['album']['images'][0]['url']
    )


def search_spotify(track_id: str) -> dict:
    spotify = Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=getenv('SPOTIFY_CLIENT_ID'),
            client_secret=getenv('SPOTIFY_CLIENT_SECRET')
        )
    )
    return spotify.track(track_id=track_id)
