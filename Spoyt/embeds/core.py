# -*- coding: utf-8 -*-
from Spoyt.embeds.definitions import BaseDiscordEmbed, BaseGuildedEmbed, EmbedDict
from Spoyt.env_check import current_platform, is_discord, is_guilded
from Spoyt.logging import log


def create_embed(data: EmbedDict) -> BaseDiscordEmbed or BaseGuildedEmbed:
    embed = BaseDiscordEmbed if is_discord() else BaseGuildedEmbed if is_guilded else None
    if type(embed) is None:
        log.critical(f'Platform is "{current_platform()}" which is not good.')
        return

    embed = embed(
        title=data.title,
        description=data.description,
        color=data.color
    )
    for field in data.fields:
        embed.add_field(
            name=field.name,
            value=field.value,
            inline=field.inline
        )
    if url := data.thumbnail_url:
        embed.set_thumbnail(url=url)
