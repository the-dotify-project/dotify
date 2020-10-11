import logging
import re

from spotdl import Spotdl, util
from spotdl.helpers.spotify import SpotifyHelpers
from spotdl.metadata_search import MetadataSearch

from spotify.settings import DEFAULT

util.install_logger(logging.INFO)


class Spotify(Spotdl):
    def __init__(self, **kwargs):
        super().__init__({**DEFAULT, **kwargs})

        self.logger = logging.getLogger(self.__class__.__name__)

    def __enter__(self):
        self.tools = SpotifyHelpers()
        return self

    def __exit__(self, exc_type, exc_value, exc_trace):
        del self.tools

        if exc_type is not None:
            self.logger.exception(f'{exc_type.__name__}: {exc_value}')

    def assert_valid_uri(self, regex, uri, message):
        assert re.match(regex, uri) is not None, message

    def assert_track_uri(self, uri):
        self.assert_valid_uri(
            r"https://open.spotify.com/track/.+",
            uri,
            f'{uri} is not a valid spotify track uri'
        )

    def assert_album_uri(self, uri):
        self.assert_valid_uri(
            r"https://open.spotify.com/album/.+",
            uri,
            f'{uri} is not a valid spotify album uri'
        )

    def assert_playlist_uri(self, uri):
        self.assert_valid_uri(
            r"https://open.spotify.com/playlist/.+",
            uri,
            f'{uri} is not a valid spotify playlist uri'
        )

    def get_tracks(self, tracks):
        urls = []
        while True:
            for item in tracks["items"]:
                track = item["track"] if "track" in item else item

                if track is None:
                    continue

                try:
                    urls.append(track["external_urls"]["spotify"])
                except KeyError:
                    self.logger.warning(f"Ignoring local track {track}")

            if not tracks["next"]:
                break

            tracks = self.tools.spotify.next(tracks)

        return urls

    def minimal_track_metadata(self, metadata):
        return {
            "uri": metadata["external_urls"]["spotify"],
            "name": metadata["name"],
            "album": {
                "name": metadata["album"]["name"],
                "uri": metadata["album"]["external_urls"]["spotify"],
            },
            "artist": {
                "name": metadata["artists"][0]["name"],
                "uri": metadata["artists"][0]["external_urls"]["spotify"],
            },
        }

    def minimal_album_metadata(self, metadata):
        return {
            "uri": metadata["external_urls"]["spotify"],
            "name": metadata["name"],
            "artist": {
                "name": metadata["artists"][0]["name"],
                "uri": metadata["artists"][0]["external_urls"]["spotify"],
            },
        }

    def minimal_playlist_metadata(self, metadata):
        return {
            'name': metadata['name']
        }

    def get_track_metadata(self, uri):
        self.assert_track_uri(uri)

        searcher = MetadataSearch(
            uri,
            lyrics=not self.arguments["no_metadata"],
            yt_search_format=self.arguments["search_format"],
            yt_manual=self.arguments["manual"],
        )

        metadata = searcher.on_youtube_and_spotify()

        return self.minimal_track_metadata(metadata)

    def fetch_playlist(self, uri):
        self.assert_playlist_uri(uri)

        metadata = self.tools.fetch_playlist(uri)

        return (
            self.minimal_playlist_metadata(metadata),
            self.get_tracks(metadata["tracks"]),
        )

    def fetch_album(self, uri):
        self.assert_album_uri(uri)

        metadata = self.tools.fetch_album(uri)

        return (
            self.minimal_album_metadata(metadata),
            self.get_tracks(self.tools.spotify.album_tracks(metadata["id"])),
        )

    def download_track(self, uri):
        self.assert_track_uri(uri)

        search_metadata = MetadataSearch(
            uri,
            lyrics=not self.arguments["no_metadata"],
            yt_search_format=self.arguments["search_format"],
            yt_manual=self.arguments["manual"],
        )

        if self.arguments["no_metadata"]:
            metadata = search_metadata.on_youtube()
        else:
            metadata = search_metadata.on_youtube_and_spotify()

        if not metadata:
            raise ValueError(f"Failed to retrieve metadata for `{uri}`")

        return (
            self.download_track_from_metadata(metadata),
            self.minimal_track_metadata(metadata),
        )

    def download_tracks(self, uris):
        for uri in uris:
            self.logger.info(f'Downloading "{uri}"')

            try:
                yield self.download_track(uri)
            except Exception as e:
                self.logger.exception(e)

                yield None, None
