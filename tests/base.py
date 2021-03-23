from pathlib import Path
from re import sub
from shutil import rmtree
from unittest import TestCase

from dotify import Album, Dotify, Playlist, Track
from tests.settings import DOTIFY_SETTINGS


class DotifyBaseTestCase(TestCase):
    """ """
    def setUp(self):
        """ """
        self.client = Dotify(
            DOTIFY_SETTINGS['spotify_id'],
            DOTIFY_SETTINGS['spotify_secret']
        )

        self.test_directory = Path(__file__).parent / 'tmp'
        self.test_directory.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        """ """
        rmtree(self.test_directory)

    @staticmethod
    def get_download_basename_track(track):
        """

        :param track: 

        
        """
        artist, name = track.artist.name, track.name
        artist, name = artist.strip(), name.strip()
        artist, name = sub(r'\s+', '_', artist), sub(r'\s+', '_', name)

        return f'{artist} - {name}.mp3'

    @staticmethod
    def get_download_basename_playlist(playlist):
        """

        :param playlist: 

        
        """
        name = playlist.name
        name = name.strip()
        name = sub(r'\s+', ' ', name)

        return name

    @staticmethod
    def get_download_basename_album(album):
        """

        :param album: 

        
        """
        artist, name = album.artist.name, album.name
        artist, name = artist.strip(), name.strip()
        artist, name = sub(r'\s+', ' ', artist), sub(r'\s+', ' ', name)

        return f'{artist} - {name}'

    @staticmethod
    def get_value(obj, attribute_path):
        """

        :param obj: 
        :param attribute_path: 

        
        """
        def get_value_recursive(obj, paths):
            """

            :param obj: 
            :param paths: 

            
            """
            if len(paths) > 0:
                return get_value_recursive(getattr(obj, paths[0]), paths[1:])

            return obj

        return get_value_recursive(obj, list(filter(None, attribute_path.split('.'))))

    def get_download_basename(self, obj):
        """

        :param obj: 

        
        """
        if isinstance(obj, Track):
            return self.get_download_basename_track(obj)
        elif isinstance(obj, Playlist):
            return self.get_download_basename_playlist(obj)
        elif isinstance(obj, Album):
            return self.get_download_basename_album(obj)
        else:
            raise RuntimeError(f'`{obj}` is an instance of {type(obj)}')

    def download(self, cls_name, url):
        """

        :param cls_name: 
        :param url: 

        
        """
        cls = getattr(self.client, cls_name)

        obj = cls.from_url(url)

        download_basename = self.get_download_basename(obj)
        download_fullpath = self.test_directory / download_basename

        obj.download(download_fullpath)

        self.assertTrue(download_fullpath.exists())

    def search(self, cls_name, query, metadata_list, limit=1):
        """

        :param cls_name: 
        :param query: 
        :param metadata_list: 
        :param limit:  (Default value = 1)

        
        """
        self.assertEqual(len(metadata_list), limit)

        cls = getattr(self.client, cls_name)

        for result, metadata in zip(cls.search(query, limit=limit), metadata_list):
            for name, value in metadata.items():
                with self.subTest('Asserting metadata equality', **{name: value}):
                    self.assertEqual(self.get_value(result, name), value)
