# -*- coding: utf-8 -*-

"""
netease-dl.exceptions
~~~~~~~~~~~~~~~~~~~~~

This module contains the set of netease-dl's exceptions.
"""
from requests.exceptions import RequestException


class SearchNotFound(RequestException):
    """Search api return None."""


class SongNotAvailable(RequestException):
    """Some songs are not available, for example Taylor Swift's songs."""


class GetRequestIllegal(RequestException):
    """Status code is not 200."""


class PostRequestIllegal(RequestException):
    """Status code is not 200."""
