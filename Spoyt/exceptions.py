# -*- coding: utf-8 -*-
class SpoytException(BaseException):
    def __init__(self, traceback='') -> None:
        message = 'Spoyt global exception'
        BaseException.__init__(self, f'{__class__.__name__}: {traceback or message}')


class YouTubeException(SpoytException):
    def __init__(self, traceback='') -> None:
        message = 'There was an error during querying YouTube.'
        SpoytException.__init__(self, f'{__class__.__name__}: {traceback or message}')


class YouTubeForbiddenException(YouTubeException):
    def __init__(self, traceback='') -> None:
        message = 'Bot is not set properly. Ask the bot owner for further information.'
        YouTubeException.__init__(self, f'{__class__.__name__}: {traceback or message}')


class SpotifyException(SpoytException):
    def __init__(self, traceback='') -> None:
        message = 'There was an error during querying Spotify.'
        SpoytException.__init__(self, f'{__class__.__name__}: {traceback or message}')



class SpotifyUnreachableException(SpotifyException):
    def __init__(self, traceback='') -> None:
        message = 'Spotify is unreachable.'
        SpotifyException.__init__(self, f'{__class__.__name__}: {traceback or message}')


class SpotifyNotFoundException(SpotifyException):
    def __init__(self, traceback='') -> None:
        message = 'Spotify track not found.'
        SpotifyException.__init__(self, f'{__class__.__name__}: {traceback or message}')
