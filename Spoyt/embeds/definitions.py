# -*- coding: utf-8 -*-
from discord import Embed as DiscordEmbed, Color as DiscordColor
from guilded import Embed as GuiledEmbed, Color as GuildedColor

from Spoyt.embeds.color import DEFAULT, DARK_RED, GREEN, RED, GOLD
from Spoyt.env_check import is_discord, is_guilded
from Spoyt.spotify_api import Playlist, Track
from Spoyt.youtube_api import YouTubeResult


MAX_QUERY = 10


class BaseDiscordEmbed(DiscordEmbed):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if 'color' not in kwargs.keys():
            self.color = DiscordColor.blurple()


class BaseGuildedEmbed(GuiledEmbed):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if 'color' not in kwargs.keys():
            self.color = GuildedColor.gilded()


class EmbedField:
    def __init__(
            self,
            name: str,
            value: str,
            inline: bool = True
    ) -> None:
        self.name = name
        self.value = value
        self.inline = inline


class EmbedDict:
    def __init__(
            self,
            title: str = None,
            description: str = None,
            color: int = DEFAULT,
            thumbnail_url: str = None
    ) -> None:
        self.title = title
        self.description = description
        self.color = color
        self._fields = []
        self.thumbnail_url = thumbnail_url

    def add_field(self, name: str, value: str, inline: bool = True) -> None:
        self._fields.append(EmbedField(name, value, inline))

    @property
    def fields(self) -> list[EmbedField]:
        return self._fields.copy()


def markdown_url(url: str) -> str:
    return (
        '<{0}>' if is_discord() else
        '[{0}]({0})' if is_guilded() else
        '{0}'
    ).format(url)


def track_to_embed(track: Track) -> EmbedDict:
    em = EmbedDict(
        title=track.name,
        description=markdown_url(track.track_url),
        color=GREEN,
        thumbnail_url=track.cover_url
    )
    em.add_field(
        name='Artist{}'.format('' if track.is_single_artist else 's'),
        value=', '.join(track.artists),
        inline=track.is_single_artist
    )
    em.add_field(
        name='Released',
        value=track.release_date
    )
    return em


def playlist_to_embed(playlist: Playlist) -> EmbedDict:
    if (d := playlist.description):
        description = f'{d}\n\n{playlist.url}'
    else:
        description = playlist.playlist_url
    em = EmbedDict(
        title=playlist.name,
        description=description,
        color=GREEN,
        thumbnail_url=playlist.cover_url
    )
    em.add_field(
        name='Owner',
        value=f'[{playlist.owner_name}]({playlist.owner_url})',
        inline=False
    )
    first_tracks = '\n'.join(map(
        lambda a: f'- [{a.name}]({a.track_url})',
        playlist.tracks[:MAX_QUERY]
    ))
    if (tr := playlist.total_tracks) > MAX_QUERY:
        first_tracks += f'\nAnd {tr - MAX_QUERY} more.'
    em.add_field(
        name='Tracks',
        value=first_tracks
    )
    return em


def video_to_embed(video: YouTubeResult) -> EmbedDict:
    return EmbedDict(
        title=video.title,
        description=markdown_url(video.video_link),
        fields=[
            EmbedField(
                name='Description',
                value=video.description,
                inline=False
            ),
            EmbedField(
                name='Published',
                value=video.published_date
            )
        ],
        thumbnail_url=video.video_thumbnail
    )


LINK_FOUND = EmbedDict(
    title='\u23f3 Spotify link found!',
    description='Connecting to super secret database\u2026',
    color=GREEN
)

SPOTIFY_UNREACHABLE = EmbedDict(
    title='Oh no',
    description='Spotify is out of service',
    color=RED
)

SEARCHING_YOUTUBE = EmbedDict(
    title='\u23f3 Searching YouTube'
)

VIDEO_NOT_FOUND = EmbedDict(
    title='Video not found',
    color=DARK_RED
)

FUNCTION_NOT_AVAILABLE = EmbedDict(
    title='\u274c Function is currently unavailable',
    color=DARK_RED
)

FUNCTION_IN_DEVELOPMENT = EmbedDict(
    title='\U0001f6e0 Function is under construction',
    description='Please check debug console for output',
    color=GOLD
)
