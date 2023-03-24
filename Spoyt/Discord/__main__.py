# -*- coding: utf-8 -*-
from logging import INFO, basicConfig

from discord import Activity, ActivityType, Client, Intents
from rich.logging import RichHandler

from Spoyt.logging import log
from Spoyt.wrapper import main

if __name__ == '__main__':
    basicConfig(
        level=INFO,
        format='%(message)s',
        datefmt='[%x]',
        handlers=[RichHandler(rich_tracebacks=True)]
    )
    log.info('Starting Discord bot')
    intents = Intents.default()
    intents.message_content = True
    client = Client(
        max_messages=None,
        intents=intents,
        activity=Activity(
            name='Spotify & YouTube',
            type=ActivityType.listening
        )
    )
    main(client, __package__)
