"""
Test
"""
import pprint

from requests.exceptions import RequestException

from .weapi import Crawler
from .utils import NetEase
from .exceptions import SearchNotFound


class TestCrawler(object):
    """Test Netease Music API."""

    def test_login():
        """Test whether phone login is avalable."""
        Crawler().login()

    def test_search_song(name):
        """Test whether the search api is available."""
        result = Crawler().search_song(name)
        pprint.pprint(result)

    def test_search_album(name):
        """Test whether the search api is available."""
        result = Crawler().search_album(name)
        pprint.pprint(result)

    def test_search_artist(name):
        """Test whether the search api is available."""
        result = Crawler().search_artist(name)
        pprint.pprint(result)

    def test_get_user_playlists(id):
        """Test whether it can return a uses's playlist if we pass the user's id."""
        result = Crawler().get_user_playlists(id)
        pprint.pprint(result)

    def test_get_playlist_songs(id):
        """Test whether it can return a specific public playlist's all songs."""
        result = Crawler().get_playlist_songs(id)
        pprint.pprint(result)

    def test_get_song_url(id):
        """Test whether it can return a song url if we pass the song'id."""
        result = Crawler().get_song_url(id)  # Love story is not available
        print(result)

    def test_get_album_songs(id):
        """Test whether it can return a album's song."""
        result = Crawler().get_album_songs(id)  # 1989 => Taylor Swift
        pprint.pprint(result)

    def test_get_artist_hot_songs(id):
        """Test whether it can return a artist's hot songs."""
        result = Crawler().get_artists_hot_songs(id)
        pprint.pprint(result)


class TestNetEase(object):
    """Test download operation."""

    def test_download_song_by_search(name):
        """Test whether downloading a sigle song is available."""
        NetEase().download_song_by_search(name)

    def test_download_album_by_search(name):
        """Test whether downloading a sigle song is available."""
        NetEase().download_album_by_search(name)

    def test_download_playlist_by_id(id):
        """Test whether downloading a playlist's songs is available."""
        NetEase().download_playlist_by_id(id)

    def test_download_artist_hot_songs(name):
        """Test whether downloading a playlist's songs is available."""
        NetEase().download_artist_hot_songs(name)

    def test_download_user_playlist():
        NetEase().download_person_playlist()


if __name__ == '__main__':
    try:
        TestNetEase.test_download_album_by_search('范特西')
    except RequestException as exception:
        print(exception)
    except SearchNotFound as exception:
        print(exception)
