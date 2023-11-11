# -*- coding: utf-8 -*-
from discord import Color as DiscordColor
from guilded import Color as GuildedColor

from Spoyt.env_check import is_discord, is_guilded

if is_discord():
    DEFAULT = DiscordColor.blurple()
elif is_guilded():
    DEFAULT = GuildedColor.gilded()
else:
    DEFAULT = 0xCCCCCC

GREEN = 0x2ECC71
RED = 0xFF0000
DARK_RED = 0x992D22
GOLD = 0xFFCC00
