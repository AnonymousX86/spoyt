# -*- coding: utf-8 -*-
from Spoyt.logger import log
from Spoyt.settings import BOT_TOKEN, SPOTIFY_CLIENT_ID, \
    SPOTIFY_CLIENT_SECRET, YOUTUBE_API_KEY


def markdown_url(url: str, text: str = None) -> str:
    """Wraps URL to be clickable with with optional mask."""
    return f'[{text}]({url})' if text else f'<{url}>'


def check_env() -> bool:
    """Checks if all required environment varables are set."""
    env_is_valid = True
    for key in [
        BOT_TOKEN,
        SPOTIFY_CLIENT_ID,
        SPOTIFY_CLIENT_SECRET,
        YOUTUBE_API_KEY
    ]:
        if not key:
            env_is_valid = False
            log.critical(f'"{key}" environment varaible is not set')
    return env_is_valid
