# -*- coding: utf-8 -*-

"""
netease-dl.weapi
~~~~~~~~~~~~~~~~

This module provides a Crawler class to get NetEase Music API.
"""
import re
import hashlib
import os
import sys

import click
import requests
from requests.exceptions import RequestException, Timeout, ProxyError
from requests.exceptions import ConnectionError as ConnectionException

from .compat import cookielib
from .encrypt import encrypted_request
from .utils import Display
from .config import headers, cookie_path, person_info_path
from .logger import get_logger
from .exceptions import (
    SearchNotFound, SongNotAvailable, GetRequestIllegal, PostRequestIllegal)
from .models import Song, Album, Artist, Playlist, User


LOG = get_logger(__name__)


def exception_handle(method):
    """Handle exception raised by requests library."""

    def wrapper(*args, **kwargs):
        try:
            result = method(*args, **kwargs)
            return result
        except ProxyError:
            LOG.exception('ProxyError when try to get %s.', args)
            raise ProxyError('A proxy error occurred.')
        except ConnectionException:
            LOG.exception('ConnectionError when try to get %s.', args)
            raise ConnectionException('DNS failure, refused connection, etc.')
        except Timeout:
            LOG.exception('Timeout when try to get %s', args)
            raise Timeout('The request timed out.')
        except RequestException:
            LOG.exception('RequestException when try to get %s.', args)
            raise RequestException('Please check out your network.')

    return wrapper


class Crawler(object):
    """NetEase Music API."""

    def __init__(self, timeout=60, proxy=None):
        self.session = requests.Session()
        self.session.headers.update(headers)
        self.session.cookies = cookielib.LWPCookieJar(cookie_path)
        self.download_session = requests.Session()
        self.timeout = timeout
        self.proxies = {'http': proxy, 'https': proxy}

        self.display = Display()

    @exception_handle
    def get_request(self, url):
        """Send a get request.

        warning: old api.
        :return: a dict or raise Exception.
        """

        resp = self.session.get(url, timeout=self.timeout,
                                proxies=self.proxies)
        result = resp.json()
        if result['code'] != 200:
            LOG.error('Return %s when try to get %s', result, url)
            raise GetRequestIllegal(result)
        else:
            return result

    @exception_handle
    def post_request(self, url, params):
        """Send a post request.

        :return: a dict or raise Exception.
        """

        data = encrypted_request(params)
        resp = self.session.post(url, data=data, timeout=self.timeout,
                                 proxies=self.proxies)
        result = resp.json()
        if result['code'] != 200:
            LOG.error('Return %s when try to post %s => %s',
                      result, url, params)
            raise PostRequestIllegal(result)
        else:
            return result

    def search(self, search_content, search_type, limit=9):
        """Search entrance.

        :params search_content: search content.
        :params search_type: search type.
        :params limit: result count returned by weapi.
        :return: a dict.
        """

        url = 'http://music.163.com/weapi/cloudsearch/get/web?csrf_token='
        params = {'s': search_content, 'type': search_type, 'offset': 0,
                  'sub': 'false', 'limit': limit}
        result = self.post_request(url, params)
        return result

    def search_song(self, song_name, quiet=False, limit=9):
        """Search song by song name.

        :params song_name: song name.
        :params limit: song count returned by weapi.
        :return: a Song object.
        """

        result = self.search(song_name, search_type=1, limit=limit)

        if result['result']['songCount'] <= 0:
            LOG.warning('Song %s not existed!', song_name)
            raise SearchNotFound('Song {} not existed.'.format(song_name))
        else:
            songs = result['result']['songs']
            if quiet:
                song_id, song_name = songs[0]['id'], songs[0]['name']
                song = Song(song_id, song_name)
                return song
            else:
                return self.display.select_one_song(songs)

    def search_album(self, album_name, quiet=False, limit=9):
        """Search album by album name.

        :params album_name: album name.
        :params limit: album count returned by weapi.
        :return: a Album object.
        """

        result = self.search(album_name, search_type=10, limit=limit)

        if result['result']['albumCount'] <= 0:
            LOG.warning('Album %s not existed!', album_name)
            raise SearchNotFound('Album {} not existed'.format(album_name))
        else:
            albums = result['result']['albums']
            if quiet:
                album_id, album_name = albums[0]['id'], albums[0]['name']
                album = Album(album_id, album_name)
                return album
            else:
                return self.display.select_one_album(albums)

    def search_artist(self, artist_name, quiet=False, limit=9):
        """Search artist by artist name.

        :params artist_name: artist name.
        :params limit: artist count returned by weapi.
        :return: a Artist object.
        """

        result = self.search(artist_name, search_type=100, limit=limit)

        if result['result']['artistCount'] <= 0:
            LOG.warning('Artist %s not existed!', artist_name)
            raise SearchNotFound('Artist {} not existed.'.format(artist_name))
        else:
            artists = result['result']['artists']
            if quiet:
                artist_id, artist_name = artists[0]['id'], artists[0]['name']
                artist = Artist(artist_id, artist_name)
                return artist
            else:
                return self.display.select_one_artist(artists)

    def search_playlist(self, playlist_name, quiet=False, limit=9):
        """Search playlist by playlist name.

        :params playlist_name: playlist name.
        :params limit: playlist count returned by weapi.
        :return: a Playlist object.
        """

        result = self.search(playlist_name, search_type=1000, limit=limit)

        if result['result']['playlistCount'] <= 0:
            LOG.warning('Playlist %s not existed!', playlist_name)
            raise SearchNotFound('playlist {} not existed'.format(playlist_name))
        else:
            playlists = result['result']['playlists']
            if quiet:
                playlist_id, playlist_name = playlists[0]['id'], playlists[0]['name']
                playlist = Playlist(playlist_id, playlist_name)
                return playlist
            else:
                return self.display.select_one_playlist(playlists)

    def search_user(self, user_name, quiet=False, limit=9):
        """Search user by user name.

        :params user_name: user name.
        :params limit: user count returned by weapi.
        :return: a User object.
        """

        result = self.search(user_name, search_type=1002, limit=limit)

        if result['result']['userprofileCount'] <= 0:
            LOG.warning('User %s not existed!', user_name)
            raise SearchNotFound('user {} not existed'.format(user_name))
        else:
            users = result['result']['userprofiles']
            if quiet:
                user_id, user_name = users[0]['userId'], users[0]['nickname']
                user = User(user_id, user_name)
                return user
            else:
                return self.display.select_one_user(users)

    def get_user_playlists(self, user_id, limit=1000):
        """Get a user's all playlists.

        warning: login is required for private playlist.
        :params user_id: user id.
        :params limit: playlist count returned by weapi.
        :return: a Playlist Object.
        """

        url = 'http://music.163.com/weapi/user/playlist?csrf_token='
        csrf = ''
        params = {'offset': 0, 'uid': user_id, 'limit': limit,
                  'csrf_token': csrf}
        result = self.post_request(url, params)
        playlists = result['playlist']
        return self.display.select_one_playlist(playlists)

    def get_playlist_songs(self, playlist_id, limit=1000):
        """Get a playlists's all songs.

        :params playlist_id: playlist id.
        :params limit: length of result returned by weapi.
        :return: a list of Song object.
        """

        url = 'http://music.163.com/weapi/v3/playlist/detail?csrf_token='
        csrf = ''
        params = {'id': playlist_id, 'offset': 0, 'total': True,
                  'limit': limit, 'n': 1000, 'csrf_token': csrf}
        result = self.post_request(url, params)

        songs = result['playlist']['tracks']
        songs = [Song(song['id'], song['name']) for song in songs]
        return songs

    def get_album_songs(self, album_id):
        """Get a album's all songs.

        warning: use old api.
        :params album_id: album id.
        :return: a list of Song object.
        """

        url = 'http://music.163.com/api/album/{}/'.format(album_id)
        result = self.get_request(url)

        songs = result['album']['songs']
        songs = [Song(song['id'], song['name']) for song in songs]
        return songs

    def get_artists_hot_songs(self, artist_id):
        """Get a artist's top50 songs.

        warning: use old api.
        :params artist_id: artist id.
        :return: a list of Song object.
        """
        url = 'http://music.163.com/api/artist/{}'.format(artist_id)
        result = self.get_request(url)

        hot_songs = result['hotSongs']
        songs = [Song(song['id'], song['name']) for song in hot_songs]
        return songs

    def get_song_url(self, song_id, bit_rate=320000):
        """Get a song's download address.

        :params song_id: song id<int>.
        :params bit_rate: {'MD 128k': 128000, 'HD 320k': 320000}
        :return: a song's download address.
        """

        url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
        csrf = ''
        params = {'ids': [song_id], 'br': bit_rate, 'csrf_token': csrf}
        result = self.post_request(url, params)
        song_url = result['data'][0]['url']  # download address

        if song_url is None:  # Taylor Swift's song is not available
            LOG.warning(
                'Song %s is not available due to copyright issue. => %s',
                song_id, result)
            raise SongNotAvailable(
                'Song {} is not available due to copyright issue.'.format(song_id))
        else:
            return song_url

    def get_song_lyric(self, song_id):
        """Get a song's lyric.

        warning: use old api.
        :params song_id: song id.
        :return: a song's lyric.
        """

        url = 'http://music.163.com/api/song/lyric?os=osx&id={}&lv=-1&kv=-1&tv=-1'.format(  # NOQA
            song_id)
        result = self.get_request(url)
        if 'lrc' in result and result['lrc']['lyric'] is not None:
            lyric_info = result['lrc']['lyric']
        else:
            lyric_info = 'Lyric not found.'
        return lyric_info

    @exception_handle
    def get_song_by_url(self, song_url, song_name, folder, lyric_info):
        """Download a song and save it to disk.

        :params song_url: download address.
        :params song_name: song name.
        :params folder: storage path.
        :params lyric: lyric info.
        """

        if not os.path.exists(folder):
            os.makedirs(folder)
        fpath = os.path.join(folder, song_name+'.mp3')

        if not os.path.exists(fpath):
            resp = self.download_session.get(
                song_url, timeout=self.timeout, stream=True)
            length = int(resp.headers.get('content-length'))
            label = 'Downlaoding {} {}kb'.format(song_name, int(length/1024))

            with click.progressbar(length=length, label=label) as progressbar:
                with open(fpath, 'wb') as song_file:
                    for chunk in resp.iter_content(chunk_size=1024):
                        if chunk:  # filter out keep-alive new chunks
                            song_file.write(chunk)
                            progressbar.update(1024)

        if lyric_info:
            folder = os.path.join(folder, 'lyric')
            if not os.path.exists(folder):
                os.makedirs(folder)
            fpath = os.path.join(folder, song_name+'.lrc')
            with open(fpath, 'w') as lyric_file:
                lyric_file.write(lyric_info)

    def login(self):
        """Login entrance."""
        username = click.prompt('Please enter your email or phone number')
        password = click.prompt('Please enter your password', hide_input=True)

        pattern = re.compile(r'^0\d{2,3}\d{7,8}$|^1[34578]\d{9}$')
        if pattern.match(username):  # use phone number to login
            url = 'https://music.163.com/weapi/login/cellphone'
            params = {
                'phone': username,
                'password': hashlib.md5(password.encode('utf-8')).hexdigest(),
                'rememberLogin': 'true'}
        else:  # use email to login
            url = 'https://music.163.com/weapi/login?csrf_token='
            params = {
                'username': username,
                'password': hashlib.md5(password.encode('utf-8')).hexdigest(),
                'rememberLogin': 'true'}

        try:
            result = self.post_request(url, params)
        except PostRequestIllegal:
            click.echo('Password Error!')
            sys.exit(1)
        self.session.cookies.save()
        uid = result['account']['id']
        with open(person_info_path, 'w') as person_info:
            person_info.write(str(uid))
