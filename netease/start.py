# -*- coding: utf-8 -*-

"""
netease-dl.start
~~~~~~~~~~~~~~~~

Entrance of netease-dl.
"""
import signal
import sys

import click

from .download import NetEase
from .logger import get_logger


LOG = get_logger(__name__)


def signal_handler(sign, frame):
    """Capture Ctrl+C."""
    LOG.info('%s => %s', sign, frame)
    click.echo('Bye')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


@click.group()
@click.option('-t', '--timeout', type=int, default=60,
              help='Time to wait before giving up, in seconds.')
@click.option('-p', '--proxy', help='Use the specified HTTP/HTTPS/SOCKS proxy.')
@click.option('-o', '--output', type=click.Path(exists=True),
              help='Specify the storage path.')
@click.option('-q', '--quiet', is_flag=True, help='Automatically select the best one.')
@click.option('-l', '--lyric', is_flag=True, help='Download lyric.')
@click.option('-a', '--again', is_flag=True, help='Login Again.')
@click.pass_context
def cli(ctx, timeout, proxy, output, quiet, lyric, again):
    """A command tool to download NetEase-Music's songs."""
    ctx.obj = NetEase(timeout, proxy, output, quiet, lyric, again)


@cli.command()
@click.option('-n', '--name', help='Song name.')
@click.option('-i', '--id', type=int, help='Song id.')
@click.pass_obj
def song(netease, name, id):
    """Download a song by name or id."""
    if name:
        netease.download_song_by_search(name)

    if id:
        netease.download_song_by_id(id, 'song'+str(id))


@cli.command()
@click.option('-n', '--name', help='Album name.')
@click.option('-i', '--id', type=int, help='Album id.')
@click.pass_obj
def album(netease, name, id):
    """Download a album's songs by name or id."""
    if name:
        netease.download_album_by_search(name)

    if id:
        netease.download_album_by_id(id, 'album'+str(id))


@cli.command()
@click.option('-n', '--name', help='Artist name.')
@click.option('-i', '--id', type=int, help='Artist id.')
@click.pass_obj
def artist(netease, name, id):
    """Download a artist's hot songs by name or id."""
    if name:
        netease.download_artist_by_search(name)

    if id:
        netease.download_artist_by_id(id, 'artist'+str(id))


@cli.command()
@click.option('-n', '--name', help='Playlist name.')
@click.option('-i', '--id', type=int, help='Playlist id.')
@click.pass_obj
def playlist(netease, name, id):
    """Download a playlist's songs by id."""
    if name:
        netease.download_playlist_by_search(name)

    if id:
        netease.download_playlist_by_id(id, 'playlist'+str(id))


@cli.command()
@click.option('-n', '--name', help='User name.')
@click.option('-i', '--id', type=int, help='User id.')
@click.pass_obj
def user(netease, name, id):
    """Download a user\'s playlists by id."""
    if name:
        netease.download_user_playlists_by_search(name)

    if id:
        netease.download_user_playlists_by_id(id)


@cli.command()
@click.pass_obj
def me(netease):
    """Download my playlists."""
    netease.download_person_playlists()
