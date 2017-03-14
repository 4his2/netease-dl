# -*- coding: utf-8 -*-

"""
netease-dl.models
~~~~~~~~~~~~~~~~~

ORM for database in the future.
"""

class Song(object):

    def __init__(self, song_id, song_name, artist_id=None, album_id=None,
                 hot_comments=None, comment_count=None, song_lyric=None,
                 song_url=None):
        self.song_id = song_id
        self.song_name = song_name
        self.artist_id = artist_id
        self.album_id = album_id
        self.hot_comments = [] if hot_comments is None else hot_comments
        self.comment_count = 0 if comment_count is None else comment_count
        self.song_lyric = u'' if song_lyric is None else song_lyric
        self.song_url = '' if song_url is None else song_url


class Comment(object):

    def __init__(self, comment_id, content, like_count, created_time,
                 user_id=None):
        self.comment_id = comment_id
        self.content = content
        self.like_count = like_count
        self.created_time = created_time
        self.user_id = user_id


class Album(object):

    def __init__(self, album_id, album_name, artist_id=None,
                 songs=None, hot_comments=None):
        self.album_id = album_id
        self.album_name = album_name
        self.artist_id = artist_id
        self.songs = [] if songs is None else songs
        self.hot_comments = [] if hot_comments is None else hot_comments

    def add_song(self, song):
        self.songs.append(song)


class Artist(object):

    def __init__(self, artist_id, artist_name, hot_songs=None):
        self.artist_id = artist_id
        self.artist_name = artist_name
        self.hot_songs = [] if hot_songs is None else hot_songs

    def add_song(self, song):
        self.hot_songs.append(song)


class Playlist(object):

    def __init__(self, playlist_id, playlist_name, user_id=None,
                 songs=None, hot_comments=None):
        self.playlist_id = playlist_id
        self.playlist_name = playlist_name
        self.user_id = user_id
        self.songs = [] if songs is None else songs
        self.hot_comments = [] if hot_comments is None else hot_comments

    def add_song(self, song):
        self.songs.append(song)


class User(object):

    def __init__(self, user_id, user_name, songs=None, hot_comments=None):
        self.user_id = user_id
        self.user_name = user_name
        self.songs = [] if songs is None else songs
        self.hot_comments = [] if hot_comments is None else hot_comments

    def add_song(self, song):
        self.songs.append(song)
