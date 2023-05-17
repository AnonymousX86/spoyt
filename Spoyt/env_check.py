# -*- coding: utf-8 -*-
from os import environ, getenv

from Spoyt.logging import log


def current_platform() -> str:
    return getenv('PLATFORM', 'unknown')


def is_discord() -> bool:
    return current_platform() == 'discord'


def is_guilded() -> bool:
    return current_platform() == 'guilded'


def check_platform(source: str, platform: str) -> bool:
    if source.lower().endswith(platform.lower()):
        environ['PLATFORM'] = platform
        log.info(f'Automatically set "PLATFORM" to "{platform}"')
        return True
    return False


def auto_set_platform(source: str) -> bool:
    for platform in ['guilded', 'discord']:
        if check_platform(source, platform):
            return True
    return False
