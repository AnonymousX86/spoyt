# -*- coding: utf-8 -*-
from typing import TypeAlias

from discord import \
    Client       as DiscordClient,  \
    Message      as DiscordMessage, \
    Member       as DiscordMember
from guilded import \
    Client       as GuildedClient,  \
    ChatMessage  as GuildedMessage, \
    Member       as GuildedMember


CLIENT_TYPE:  TypeAlias = DiscordClient  or GuildedClient
MESSAGE_TYPE: TypeAlias = DiscordMessage or GuildedMessage
MEMBER_TYPE:  TypeAlias = DiscordMember  or GuildedMember
