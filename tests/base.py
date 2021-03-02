from pathlib import Path
from re import sub
from shutil import rmtree
from unittest import TestCase

from spotify import Album, Playlist, Spotify, Track

from tests.settings import DOTIFY_SETTINGS


class DotifyBaseTestCase(TestCase):
    def setUp(self):
        self.client = Spotify(
            DOTIFY_SETTINGS['spotify_id'],
            DOTIFY_SETTINGS['spotify_secret']
        )

        self.test_directory = Path(__file__).parent / 'tmp'
        self.test_directory.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        rmtree(self.test_directory)

    def _get_download_basename_track(self, track):
        artist, name = track.artists[0], track.name
        artist, name = artist.strip(), name.strip()
        artist, name = sub(r'\s+', '_', artist), sub(r'\s+', '_', name)

        return f'{artist} - {name}.mp3'

    def _get_download_basename_playlist(self, playlist):
        name = playlist.name
        name = name.strip()
        name = sub(r'\s+', ' ', name)

        return name

    def _get_download_basename_album(self, album):
        artist, name = album.artist.name, album.name
        artist, name = artist.strip(), name.strip()
        artist, name = sub(r'\s+', ' ', artist), sub(r'\s+', ' ', name)

        return f'{artist} - {name}'

    def get_download_basename(self, obj):
        if isinstance(obj, Track):
            return self._get_download_basename_track(obj)
        elif isinstance(obj, Playlist):
            return self._get_download_basename_playlist(obj)
        elif isinstance(obj, Album):
            return self._get_download_basename_album(obj)
        else:
            raise RuntimeError(f'`{obj}` is an instance of {type(obj)}')

    def download(self, cls, url):
        with self.client:
            obj = cls.from_url(self.client, url)

            download_basename = self.get_download_basename(obj)
            download_fullpath = self.test_directory / download_basename

            obj.download(download_fullpath)

            self.assertTrue(download_fullpath.exists())

    def search(self, cls, query, metadata):
        with self.client:
            results = next(cls.search(self.client, query, limit=1))

            self.assertEqual(results, metadata)
