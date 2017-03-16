# -*- coding: utf-8 -*-

"""
netease-dl.download
~~~~~~~~~~~~~~~~~~~

This module provides a NetEase class to directly support download operation.
"""
import os
import time
import re
import sys

import click
from requests.exceptions import RequestException

from .weapi import Crawler
from .config import person_info_path, cookie_path
from .logger import get_logger


LOG = get_logger(__name__)


def timeit(method):
    """Compute the download time."""

    def wrapper(*args, **kwargs):
        start = time.time()
        result = method(*args, **kwargs)
        end = time.time()

        click.echo('Cost {}s'.format(int(end-start)))
        return result

    return wrapper


def login(method):
    """Require user to login."""

    def wrapper(*args, **kwargs):
        crawler = args[0].crawler  # args[0] is a NetEase object

        try:
            if os.path.isfile(cookie_path):
                with open(cookie_path, 'r') as cookie_file:
                    cookie = cookie_file.read()
                expire_time = re.compile(r'\d{4}-\d{2}-\d{2}').findall(cookie)
                now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                if expire_time[0] > now:
                    crawler.session.cookies.load()
                else:
                    crawler.login()
            else:
                crawler.login()
        except RequestException:
            click.echo('Maybe password error, please try again.')
            sys.exit(1)
        result = method(*args, **kwargs)
        return result

    return wrapper


class NetEase(object):
    """Provide download operation."""

    def __init__(self, timeout, proxy, folder, quiet, lyric, again):
        self.crawler = Crawler(timeout, proxy)
        self.folder = '.' if folder is None else folder
        self.quiet = quiet
        self.lyric = lyric
        try:
            if again:
                self.crawler.login()
        except RequestException:
            click.echo('Maybe password error, please try again.')

    def download_song_by_search(self, song_name):
        """Download a song by its name.

        :params song_name: song name.
        """

        try:
            song = self.crawler.search_song(song_name, self.quiet)
        except RequestException as exception:
            click.echo(exception)
        else:
            self.download_song_by_id(song.song_id, song.song_name, self.folder)

    def download_song_by_id(self, song_id, song_name, folder='.'):
        """Download a song by id and save it to disk.

        :params song_id: song id.
        :params song_name: song name.
        :params folder: storage path.
        """

        try:
            url = self.crawler.get_song_url(song_id)
            if self.lyric:
                # use old api
                lyric_info = self.crawler.get_song_lyric(song_id)
            else:
                lyric_info = None
            song_name = song_name.replace('/', '')
            song_name = song_name.replace('.', '')
            self.crawler.get_song_by_url(url, song_name, folder, lyric_info)
        except RequestException as exception:
            click.echo(exception)

    def download_album_by_search(self, album_name):
        """Download a album by its name.

        :params album_name: album name.
        """

        try:
            album = self.crawler.search_album(album_name, self.quiet)
        except RequestException as exception:
            click.echo(exception)
        else:
            self.download_album_by_id(album.album_id, album.album_name)

    @timeit
    def download_album_by_id(self, album_id, album_name):
        """Download a album by its name.

        :params album_id: album id.
        :params album_name: album name.
        """

        try:
            # use old api
            songs = self.crawler.get_album_songs(album_id)
        except RequestException as exception:
            click.echo(exception)
        else:
            folder = os.path.join(self.folder, album_name)
            for song in songs:
                self.download_song_by_id(song.song_id, song.song_name, folder)

    def download_artist_by_search(self, artist_name):
        """Download a artist's top50 songs by his/her name.

        :params artist_name: artist name.
        """

        try:
            artist = self.crawler.search_artist(artist_name, self.quiet)
        except RequestException as exception:
            click.echo(exception)
        else:
            self.download_artist_by_id(artist.artist_id, artist.artist_name)

    @timeit
    def download_artist_by_id(self, artist_id, artist_name):
        """Download a artist's top50 songs by his/her id.

        :params artist_id: artist id.
        :params artist_name: artist name.
        """

        try:
            # use old api
            songs = self.crawler.get_artists_hot_songs(artist_id)
        except RequestException as exception:
            click.echo(exception)
        else:
            folder = os.path.join(self.folder, artist_name)
            for song in songs:
                self.download_song_by_id(song.song_id, song.song_name, folder)

    def download_playlist_by_search(self, playlist_name):
        """Download a playlist's songs by its name.

        :params playlist_name: playlist name.
        """

        try:
            playlist = self.crawler.search_playlist(
                playlist_name, self.quiet)
        except RequestException as exception:
            click.echo(exception)
        else:
            self.download_playlist_by_id(
                playlist.playlist_id, playlist.playlist_name)

    @timeit
    def download_playlist_by_id(self, playlist_id, playlist_name):
        """Download a playlist's songs by its id.

        :params playlist_id: playlist id.
        :params playlist_name: playlist name.
        """

        try:
            songs = self.crawler.get_playlist_songs(
                playlist_id)
        except RequestException as exception:
            click.echo(exception)
        else:
            folder = os.path.join(self.folder, playlist_name)
            for song in songs:
                self.download_song_by_id(song.song_id, song.song_name, folder)

    def download_user_playlists_by_search(self, user_name):
        """Download user's playlists by his/her name.

        :params user_name: user name.
        """

        try:
            user = self.crawler.search_user(user_name, self.quiet)
        except RequestException as exception:
            click.echo(exception)
        else:
            self.download_user_playlists_by_id(user.user_id)

    def download_user_playlists_by_id(self, user_id):
        """Download user's playlists by his/her id.

        :params user_id: user id.
        """

        try:
            playlist = self.crawler.get_user_playlists(user_id)
        except RequestException as exception:
            click.echo(exception)
        else:
            self.download_playlist_by_id(
                playlist.playlist_id, playlist.playlist_name)

    @login
    def download_person_playlists(self):
        """Download person playlist including private playlist.

        note: login required.
        """

        with open(person_info_path, 'r') as person_info:
            user_id = int(person_info.read())
        self.download_user_playlists_by_id(user_id)
