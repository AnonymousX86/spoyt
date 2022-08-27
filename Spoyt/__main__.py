# -*- coding: utf-8 -*-
from os import getenv

from discord import Client, Intents, Message, Embed, Color, \
    ActivityType, Activity, NotFound, Forbidden

from Spoyt.spotify_api import search_spotify, model_track, TrackEmbed
from Spoyt.youtube_api import create_youtube, search_youtube


def main():
    intents = Intents.default()
    intents.message_content = True

    client = Client(intents=intents)
    client.youtube = None

    @client.event
    async def on_ready():
        print(f'Logged in as {client.user}')
        await client.change_presence(
            activity=Activity(
                name='Spotify & YouTube',
                type=ActivityType.listening
            )
        )
        client.youtube = create_youtube()

    @client.event
    async def on_message(message: Message):
        if not message.content.startswith('https://open.spotify.com/track/'):
            return

        msg = await message.channel.send(embed=Embed(
            title=':hourglass_flowing_sand: Spotify link found!',
            description='Connecting to super secret database...',
            color=Color.green()
        ))

        track_id = message.content.split('?')[0].split('&')[0].split('/')[-1]
        spotify_query = search_spotify(track_id)

        if not spotify_query:
            await msg.edit(embed=Embed(
                title='Oh no',
                description='Spotify is out of service',
                color=Color.red()
            ))
            return

        track = model_track(spotify_query)
        track_embed = TrackEmbed(track)

        try:
            await message.delete()
        except Forbidden or NotFound:
            pass
        else:
            track_embed.add_author(message.author)

        await msg.edit(embeds=[track_embed, Embed(
            title=':hourglass_flowing_sand: Searching YouTube',
            color=Color.blurple()
        )])

        video_id = search_youtube(
            youtube=client.youtube,
            query='{} {}'.format(track.name, ' '.join(track.artists))
        )

        await msg.edit(embeds=[track_embed, Embed(
                title='Best YouTube result',
                color=Color.blurple()
        )])

        await message.channel.send(
            content=f'https://www.youtube.com/watch?v={video_id}'
        )

    client.run(getenv('BOT_TOKEN'))


if __name__ == '__main__':
    main()
