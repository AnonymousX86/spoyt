# -*- coding: utf-8 -*-
from os import getenv


def bot_token():
    return getenv('BOT_TOKEN')
