# -*- coding: utf-8 -*-
from logging import INFO, basicConfig

from rich.logging import RichHandler

from Spoyt.logging import log

if __name__ == '__main__':
    basicConfig(
        level=INFO,
        format='%(message)s',
        datefmt='[%x]',
        handlers=[RichHandler(rich_tracebacks=True)]
    )
    log.info('This is general Spoyt module.')
    log.info('To run specific bot please run "Discord" or "Guilded" module.')
    log.info('Remember to set "BOT_TOKEN" environment variables.')
