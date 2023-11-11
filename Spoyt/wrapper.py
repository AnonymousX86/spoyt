# -*- coding: utf-8 -*-
from json import dump as json_dump

from discord import \
    Forbidden as DiscordForbidden, \
    NotFound as DiscordNotFound
from guilded import \
    Forbidden as GuildedForbidden, \
    NotFound as GuildedNotFound

from Spoyt.embeds.core import create_embed
from Spoyt.embeds.definitions import FUNCTION_IN_DEVELOPMENT, \
    FUNCTION_NOT_AVAILABLE, LINK_FOUND, SEARCHING_YOUTUBE, \
    SPOTIFY_UNREACHABLE, VIDEO_NOT_FOUND, playlist_to_embed, track_to_embed, video_to_embed, \
    EmbedDict
from Spoyt.env_check import auto_set_platform, current_platform
from Spoyt.logging import log
from Spoyt.settings import bot_token
from Spoyt.spotify_api import Playlist, Track, search_track, search_playlist
from Spoyt.types import CLIENT_TYPE, MESSAGE_TYPE
from Spoyt.youtube_api import find_video_by_id


def main(client: CLIENT_TYPE, source: str = None):
    if current_platform() == 'unknown':
        if not auto_set_platform(source):
            log.critical('Please set "PLATFORM"')
            return

    log.info(f'Running on "{current_platform()}" platform')

    if bot_token() is None:
        log.critical('Please set "BOT_TOKEN"')
        return

    @client.event
    async def on_ready():
        log.info(f'Logged in as {client.user}')

    @client.event
    async def on_message(message: MESSAGE_TYPE):
        content = message.content
        # Masked links
        if content.startswith('['):
            content = content[1::].split(']')[0]
        if not content.startswith('https://open.spotify.com/'):
            return
        # Track
        if content.startswith('https://open.spotify.com/track/'):
            new_em = LINK_FOUND
            new_em.add_field(
                name='Type',
                value='track'
            )
            spotify_msg: MESSAGE_TYPE = await message.channel.send(embed=create_embed(LINK_FOUND))
            track_id = message.content.split('?')[0].split('&')[0].split('/')[-1]
            spotify_query = search_track(track_id)

            if not spotify_query:
                await spotify_msg.edit(embed=create_embed(SPOTIFY_UNREACHABLE))
                return

            track = Track(spotify_query)
            track_embed = create_embed(track_to_embed(track))
            await spotify_msg.edit(embed=track_embed)

            youtube_msg: MESSAGE_TYPE = await message.channel.send(embed=create_embed(SEARCHING_YOUTUBE))
            youtube_query = '{} {}'.format(track.name, ' '.join(track.artists))
            youtube_result = find_video_by_id(query=youtube_query)

            if not youtube_result.found:
                await youtube_msg.edit(embed=create_embed(EmbedDict(
                    **VIDEO_NOT_FOUND,
                    description=youtube_result.description,
                )))
                return

            await youtube_msg.edit(embed=create_embed(
                video_to_embed(youtube_result)
            ).set_author(
                name=f'{message.author.display_name} (probably) shared:',
                icon_url=message.author.display_avatar.url
            ))

            try:
                await message.delete()
            except DiscordForbidden or DiscordNotFound or GuildedForbidden or GuildedNotFound:
                pass
            else:
                track_embed.set_author(
                    name=f'{message.author.display_name} shared:',
                    icon_url=message.author.display_avatar.url
                )
                await spotify_msg.edit(embed=track_embed)

            log.info(f'Successfully converted "{track.name}" track')
        # Playlist
        if content.startswith('https://open.spotify.com/playlist/'):
            if current_platform() == 'guilded':
                spotify_msg: MESSAGE_TYPE = await message.channel.send(embed=create_embed(FUNCTION_NOT_AVAILABLE))
                return

            new_em = LINK_FOUND
            new_em.add_field(
                name='Type',
                value='playlist'
            )
            spotify_msg: MESSAGE_TYPE = await message.channel.send(embed=create_embed(new_em))
            playlist_id = message.content.split('?')[0].split('&')[0].split('/')[-1]
            spotify_query = search_playlist(playlist_id)

            if not spotify_query:
                await spotify_msg.edit(embed=create_embed(SPOTIFY_UNREACHABLE))
                return

            playlist = Playlist(spotify_query)
            playlist_embed = create_embed(playlist_to_embed(playlist))
            await spotify_msg.edit(embed=playlist_embed)

    client.run(bot_token())
