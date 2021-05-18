from pathlib import Path
from re import sub
from shutil import rmtree
from unittest import TestCase

import dotify.models as models
from dotify import Album, Dotify, Playlist, Track
from tests.settings import DOTIFY_SETTINGS


class DotifyBaseTestCase(TestCase):
    """ """

    def setUp(self):
        """ """
        self.client = Dotify(
            DOTIFY_SETTINGS["spotify_id"],
            DOTIFY_SETTINGS["spotify_secret"],
        )

        self.test_directory = Path(__file__).parent / "tmp"
        self.test_directory.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        """ """
        rmtree(self.test_directory)

    @classmethod
    def get_download_basename_track(cls, track):
        """"""
        artist, name = track.artist.name, track.name
        artist, name = artist.strip(), name.strip()
        artist, name = sub(r"\s+", "_", artist), sub(r"\s+", "_", name)

        return "{0} - {1}.mp3".format(artist, name)

    @classmethod
    def get_download_basename_playlist(cls, playlist):
        """"""
        return sub(r"\s+", " ", playlist.name.strip())

    @classmethod
    def get_download_basename_album(cls, album):
        """"""
        artist, name = album.artist.name, album.name
        artist, name = artist.strip(), name.strip()
        artist, name = sub(r"\s+", " ", artist), sub(r"\s+", " ", name)

        return "{0} - {1}".format(artist, name)

    @classmethod
    def get_value(cls, obj, attribute_path):
        """"""

        def get_value_recursive(_, paths):
            """"""
            if paths:
                return get_value_recursive(getattr(_, paths[0]), paths[1:])

            return _

        return get_value_recursive(obj, list(filter(None, attribute_path.split("."))))

    def get_download_basename(self, obj):
        """"""
        if isinstance(obj, Track):
            return self.get_download_basename_track(obj)
        elif isinstance(obj, Playlist):
            return self.get_download_basename_playlist(obj)
        elif isinstance(obj, Album):
            return self.get_download_basename_album(obj)

        raise RuntimeError("`{0}` is an instance of {1}".format(obj, type(obj)))

    def download(self, cls_name, url):
        """"""
        with self.client:
            model_type = getattr(models, cls_name)

            obj = model_type.from_url(url)

            download_basename = self.get_download_basename(obj)
            download_fullpath = self.test_directory / download_basename

            obj.download(download_fullpath)

            self.assertTrue(download_fullpath.exists())

    def search(self, cls_name, query, metadata_list, limit=1):
        """"""
        with self.client:
            self.assertEqual(len(metadata_list), limit)

            model_type = getattr(models, cls_name)

            for result, metadata in zip(
                model_type.search(query, limit=limit),
                metadata_list,
            ):
                for name, value in metadata.items():
                    with self.subTest("Asserting metadata equality", **{name: value}):
                        self.assertEqual(self.get_value(result, name), value)
