# -*- coding: utf-8 -*-
from logging import INFO, basicConfig

from guilded import Client
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
    log.info('Starting Guilded bot')
    client = Client()
    main(client, __package__)
