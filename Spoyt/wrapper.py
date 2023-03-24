# -*- coding: utf-8 -*-
from discord import \
    Forbidden as DiscordForbidden, \
    NotFound  as DiscordNotFound
from guilded import \
    Forbidden as GuildedForbidden, \
    NotFound  as GuildedNotFound

from Spoyt.embeds.core import create_embed
from Spoyt.embeds.definitions import LINK_FOUND, SEARCHING_YOUTUBE, SPOTIFY_UNREACHABLE, VIDEO_NOT_FOUND, track_to_embed, video_to_embed
from Spoyt.env_check import auto_set_platform, current_platfrom
from Spoyt.logging import log
from Spoyt.settings import bot_token
from Spoyt.spotify_api import model_track, search_spotify
from Spoyt.types import CLIENT_TYPE, MESSAGE_TYPE
from Spoyt.youtube_api import find_video_by_id


def main(Client: CLIENT_TYPE, source: str = None):
    if current_platfrom() == 'unknown':
        if not auto_set_platform(source):
            log.critical('Please set "PLATFORM"')
            return

    log.info(f'Running on "{current_platfrom()}" platform')

    if bot_token() is None:
        log.critical('Please set "BOT_TOKEN"')
        return

    client = Client()

    @client.event
    async def on_ready():
        log.info(f'Logged in as {client.user}')

    @client.event
    async def on_message(message: MESSAGE_TYPE):
        content = message.content
        if content.startswith('['):
            content = content[1::].split(']')[0]
        if not content.startswith('https://open.spotify.com/track/'):
            return
        
        spotify_msg: MESSAGE_TYPE = await message.channel.send(embed=create_embed(LINK_FOUND))
        track_id = message.content.split('?')[0].split('&')[0].split('/')[-1]
        spotify_query = search_spotify(track_id)

        if not spotify_query:
            await spotify_msg.edit(embed=create_embed(SPOTIFY_UNREACHABLE))
            return
        
        track = model_track(spotify_query)
        track_embed = create_embed(track_to_embed(track))
        await spotify_msg.edit(embed=track_embed)

        youtube_msg: MESSAGE_TYPE = await message.channel.send(embed=create_embed(SEARCHING_YOUTUBE))
        youtube_query = '{} {}'.format(track.name, ' '.join(track.artists))
        youtube_result = find_video_by_id(query=youtube_query)

        if not youtube_result.found:
            await youtube_msg.edit(embed=create_embed(dict(
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

        log.info(f'Successfully converted "{track.name}" track')

    client.run(bot_token())
