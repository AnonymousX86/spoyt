# -*- coding: utf-8 -*-
from logging import INFO, basicConfig

from discord import ApplicationContext, Bot, Option
from discord.ext.commands import Cooldown
from rich.logging import RichHandler

from Spoyt.api.spotify import search_track, search_playlist, url_to_id
from Spoyt.api.youtube import search_video
from Spoyt.embeds import ErrorEmbed, IncorrectInputEmbed, SpotifyTrackEmbed, \
    SpotifyPlaylistEmbed, SpotifyUnreachableEmbed, YouTubeVideoEmbed, \
        UnderCunstructionEmbed
from Spoyt.exceptions import SpotifyUnreachableException, YouTubeException
from Spoyt.logger import log
from Spoyt.settings import BOT_TOKEN
from Spoyt.utils import check_env

if __name__ == '__main__':
    basicConfig(
        level=INFO,
        format='%(message)s',
        datefmt='[%x]',
        handlers=[RichHandler(rich_tracebacks=True)]
    )
    if not check_env():
        log.critical('Aborting start')
        exit()

    log.info('Starting Discord bot')

    bot = Bot()

    @bot.event
    async def on_ready() -> None:
        log.info(f'Logged in as "{bot.user}"')

    @bot.slash_command(
        name='track',
        description='Search for a track',
        cooldown=Cooldown(
            rate=1,
            per=5.0
        ),
    )
    async def track(
        ctx: ApplicationContext,
        url: Option(
            input_type=str,
            name='url',
            description='Starts with "https://open.spotify.com/track/..."',
            required=True
        )
    ) -> None:
        if not url.startswith('https://open.spotify.com/track/'):
            await ctx.respond(embed=IncorrectInputEmbed)
            return

        track_id = url_to_id(url)
        try:
            track = search_track(track_id)
        except SpotifyUnreachableException:
            await ctx.respond(embed=SpotifyUnreachableEmbed)
            return

        await ctx.respond(embed=SpotifyTrackEmbed(track))

        youtube_query = '{} {}'.format(track.name, ' '.join(track.artists))
        try:
            youtube_result = search_video(youtube_query)
        except YouTubeException as e:
            await ctx.channel.send(embed=ErrorEmbed(
                description=f'```diff\n- {e}\n```'
            ))
            return
        await ctx.channel.send(embed=YouTubeVideoEmbed(youtube_result))

        log.info(f'Successfully converted "{track.name}" track')

    @bot.slash_command(
        name='playlist',
        description='Search for a playlist',
        cooldown=Cooldown(
            rate=1,
            per=30.0
        ),
    )
    async def playlist(
        ctx: ApplicationContext,
        url: Option(
            input_type=str,
            name='url',
            description='Starts with "https://open.spotify.com/playlist/..."',
            required=True
        )
    ) -> None:
        if not url.startswith('https://open.spotify.com/playlist/'):
            await ctx.respond(embed=IncorrectInputEmbed)
            return

        playlist_id = url_to_id(url)
        try:
            playlist = search_playlist(playlist_id)
        except SpotifyUnreachableException:
            await ctx.respond(embed=SpotifyUnreachableEmbed)
            return

        await ctx.respond(embed=SpotifyPlaylistEmbed(playlist))

        await ctx.channel.send(embed=UnderCunstructionEmbed)
        log.info('Playlist conversion issued.')

    bot.start(BOT_TOKEN)
