from unittest import TestCase
from re import sub
from pathlib import Path

from spotify import Spotify, Track, Playlist, Album
from tests.settings import DOTIFY_SETTINGS


class DotifyBaseTestCase(TestCase):
    def setUp(self):
        self.client = Spotify(
            DOTIFY_SETTINGS['spotify_id'],
            DOTIFY_SETTINGS['spotify_secret']
        )

    def download_track(self, url):
        with self.client:
            track = Track.from_url(self.client, url)

            artist, name = track.artists[0], track.name
            artist, name = artist.strip(), name.strip()
            artist, name = sub(r'\s+', '_', artist), sub(r'\s+', '_', name)

            track.download(Path.cwd() / f'{artist} - {name}.mp3')

    def download_playlist(self, url):
        with self.client:
            playlist = Playlist.from_url(self.client, url)

            name = playlist.name
            name = name.strip()
            name = sub(r'\s+', ' ', name)

            playlist.download(Path.cwd() / name)

    def download_album(self, url):
        url = 'https://open.spotify.com/album/5WEwObchJdvIzPcmm2e3Li'
        with self.client:
            album = Album.from_url(self.client, url)

            artist, name = album.artist.name, album.name
            artist, name = artist.strip(), name.strip()
            artist, name = sub(r'\s+', ' ', artist), sub(r'\s+', ' ', name)

            album.download(Path.cwd() / f'{artist} - {name}')

    def search_track(self, cls, query, metadata):
        with self.client:
            results = cls.search(self.client, query, limit=1)

            self.assertEqual(results[0], metadata)
