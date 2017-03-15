# -*- coding: utf-8 -*-

"""
netease-dl.util
~~~~~~~~~~~~~~~

This module provides a Display class to show results to user.
"""
import click
from prettytable import PrettyTable

from .models import Song, Album, Artist, Playlist, User


class Display(object):
    """Display the result in the terminal."""

    @staticmethod
    def select_one_song(songs):
        """Display the songs returned by search api.

        :params songs: API['result']['songs']
        :return: a Song object.
        """

        if len(songs) == 1:
            select_i = 0
        else:
            table = PrettyTable(['Sequence', 'Song Name', 'Artist Name'])
            for i, song in enumerate(songs, 1):
                table.add_row([i, song['name'], song['ar'][0]['name']])
            click.echo(table)

            select_i = click.prompt('Select one song', type=int, default=1)
            while select_i < 1 or select_i > len(songs):
                select_i = click.prompt('Error Select! Select Again', type=int)

        song_id, song_name = songs[select_i-1]['id'], songs[select_i-1]['name']
        song = Song(song_id, song_name)
        return song

    @staticmethod
    def select_one_album(albums):
        """Display the albums returned by search api.

        :params albums: API['result']['albums']
        :return: a Album object.
        """

        if len(albums) == 1:
            select_i = 0
        else:
            table = PrettyTable(['Sequence', 'Album Name', 'Artist Name'])
            for i, album in enumerate(albums, 1):
                table.add_row([i, album['name'], album['artist']['name']])
            click.echo(table)

            select_i = click.prompt('Select one album', type=int, default=1)
            while select_i < 1 or select_i > len(albums):
                select_i = click.prompt('Error Select! Select Again', type=int)

        album_id = albums[select_i-1]['id']
        album_name = albums[select_i-1]['name']
        album = Album(album_id, album_name)
        return album

    @staticmethod
    def select_one_artist(artists):
        """Display the artists returned by search api.

        :params artists: API['result']['artists']
        :return: a Artist object.
        """

        if len(artists) == 1:
            select_i = 0
        else:
            table = PrettyTable(['Sequence', 'Artist Name'])
            for i, artist in enumerate(artists, 1):
                table.add_row([i, artist['name']])
            click.echo(table)

            select_i = click.prompt('Select one artist', type=int, default=1)
            while select_i < 1 or select_i > len(artists):
                select_i = click.prompt('Error Select! Select Again', type=int)

        artist_id = artists[select_i-1]['id']
        artist_name = artists[select_i-1]['name']
        artist = Artist(artist_id, artist_name)
        return artist

    @staticmethod
    def select_one_playlist(playlists):
        """Display the playlists returned by search api or user playlist.

        :params playlists: API['result']['playlists'] or API['playlist']
        :return: a Playlist object.
        """

        if len(playlists) == 1:
            select_i = 0
        else:
            table = PrettyTable(['Sequence', 'Name'])
            for i, playlist in enumerate(playlists, 1):
                table.add_row([i, playlist['name']])
            click.echo(table)

            select_i = click.prompt('Select one playlist', type=int, default=1)
            while select_i < 1 or select_i > len(playlists):
                select_i = click.prompt('Error Select! Select Again', type=int)

        playlist_id = playlists[select_i-1]['id']
        playlist_name = playlists[select_i-1]['name']
        playlist = Playlist(playlist_id, playlist_name)
        return playlist

    @staticmethod
    def select_one_user(users):
        """Display the users returned by search api.

        :params users: API['result']['userprofiles']
        :return: a User object.
        """

        if len(users) == 1:
            select_i = 0
        else:
            table = PrettyTable(['Sequence', 'Name'])
            for i, user in enumerate(users, 1):
                table.add_row([i, user['nickname']])
            click.echo(table)

            select_i = click.prompt('Select one user', type=int, default=1)
            while select_i < 1 or select_i > len(users):
                select_i = click.prompt('Error Select! Select Again', type=int)

        user_id = users[select_i-1]['userId']
        user_name = users[select_i-1]['nickname']
        user = User(user_id, user_name)
        return user
