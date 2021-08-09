import contextlib
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any, AnyStr, Dict, Iterator, List, Optional, cast
from urllib.error import HTTPError

from moviepy.editor import AudioFileClip
from mutagen.easyid3 import EasyID3
from pytube import YouTube
from pytube.streams import Stream
from youtubesearchpython import VideosSearch

from dotify._model import Model, logger

logger = logging.getLogger("{0}.{1}".format(logger.name, __name__))

EasyID3.RegisterTextKey("albumcover", "APIC")

if TYPE_CHECKING is True:
    from dotify.models._artist import Artist


class TrackBase(Model):
    """`TrackBase` defines the interface of the `Track` class, which is subclassing it."""

    class Json(object):
        abstract = True

    def __str__(self) -> str:
        return "{0} - {1}".format(self.artist, self.name)

    @property
    def url(self) -> AnyStr:
        """Return the track's Spotify URL.

        Returns:
            AnyStr: the URL in string format
        """
        return cast(AnyStr, self.external_urls.spotify)

    @property
    def artist(self) -> "Artist":
        """Return the track's artist.

        Returns:
            Artist: an instance of `Artist` representing the track's artist relevant info
        """
        return cast("Artist", self.artists[0])

    @property
    def genres(self) -> List[str]:
        """Return the track's genres.

        Returns:
            List[str]: a list containing the track's genres
        """
        genres = []
        for item in (self.album, self.artist):
            with contextlib.suppress(AttributeError):
                genres.append(item.genres)

        return genres

    @property
    def genre(self) -> Optional[str]:
        """Return the track's main genre.

        Returns:
            Optional[str]: the track's main genre
        """
        with contextlib.suppress(IndexError):
            return self.genres[0]

        return None

    @classmethod
    @Model.validate_url
    @Model.http_safeguard
    def from_url(cls, url: AnyStr) -> "Track":
        """Return a `Track` given its corresponding Spotify URL.

        Args:
            url (AnyStr): the Spotify URL of the track

        Returns:
            Track: the corresponding track
        """
        return cls(**cls.context.track(url))


class Track(TrackBase):
    """`Track` implements the track downloading logic."""

    class Json(object):
        dependencies = [
            "dotify.models.Album",
            "dotify.models.Artist",
            "dotify.models.Image",
        ]

    def streams(self, limit: Optional[int] = 1) -> Iterator[Stream]:
        """Yield the track's corresponding YouTube search results audio streams.

        Args:
            limit (Optional[int]): the desired number of search result items. Defaults to 1.

        Yields:
            Iterator[Stream]: yields each one of the search result audio streams
        """
        results = VideosSearch(str(self), limit=limit).result()["result"]

        yield from (YouTube(result["link"]).streams.get_audio_only() for result in results)

    @property
    def stream(self) -> Stream:
        """Return the audio stream corresponding to the the top search result.

        Returns:
            Stream: an audio stream of the track
        """
        return next(self.streams(limit=1))

    @property
    def id3_tags(self) -> Dict[str, Any]:
        """Recover the track's `ID3` tags.

        Returns:
            Dict[str, Any]: a dictionary containing the track's `ID3` tags
        """
        optional: Dict[str, Any] = {}
        if self.genre is not None:
            optional["genre"] = self.genre

        return {
            **optional,
            "title": self.name,
            "titlesort": self.name,
            "tracknumber": str(self.track_number),
            "artist": [artist.name for artist in self.artists],
            "album": self.album.name,
            "albumartist": [artist.name for artist in self.album.artists],
            "date": self.album.release_date,
            "originaldate": self.album.release_date,
            "albumcover": self.album.cover,
        }

    def as_mp4(self, mp4_path: Path, skip_existing: Optional[bool] = False) -> Path:
        """Download the track in `.mp4` format.

        Args:
            mp4_path (Path): where should the resulting file be stored
            skip_existing (Optional[bool]): whether or not to overwrite an
                existing file. Defaults to False.

        Raises:
            NotFound: if no audio stream corresponding to the track at hand is found

        Returns:
            Path: the download location of the `.mp4` file
        """
        mp4_path = Path(mp4_path)

        try:
            return Path(
                self.stream.download(
                    output_path=mp4_path.parent,
                    filename=mp4_path.stem,
                    skip_existing=skip_existing,
                ),
            )
        except HTTPError as http_error:
            raise self.NotFound() from http_error

    def as_mp3(
        self,
        mp3_path: Path,
        skip_existing: Optional[bool] = False,
        progress_logger: Optional[logging.Logger] = None,
    ) -> Path:
        """Download the track in `.mp3` format.

        Args:
            mp3_path (Path): where should the resulting file be stored
            skip_existing (Optional[bool]): whether or not to overwrite
                an existing file. Defaults to False.
            progress_logger (Optional[logging.Logger]): a logger reporting
                on the download progress. Defaults to None.

        Returns:
            Path: the download location of the `.mp3` file
        """
        # FIXME: genres
        # FIXME: progress bar and logging both for moviepy and pytube

        mp3_path = Path(mp3_path)

        mp4_path = self.as_mp4(mp3_path, skip_existing=skip_existing)

        audio_file_clip = AudioFileClip(str(mp4_path))
        audio_file_clip.write_audiofile(str(mp3_path), logger=progress_logger)

        mp4_path.unlink()

        easy_id3 = EasyID3(mp3_path)

        easy_id3.update(self.id3_tags)

        easy_id3.save(v2_version=3)

        return mp3_path

    def download(
        self,
        mp3_path: Path,
        skip_existing: Optional[bool] = False,
        progress_logger: Optional[logging.Logger] = None,
    ) -> Path:
        """Download the track in `.mp3` format.

        Args:
            mp3_path (Path): where should the resulting file be stored
            skip_existing (Optional[bool]): whether or not to overwrite an
                existing file. Defaults to False.
            progress_logger (Optional[logging.Logger]): a logger reporting
                on the download progress. Defaults to None.

        Returns:
            Path: the download location of the `.mp3` file
        """
        return self.as_mp3(
            mp3_path,
            skip_existing=skip_existing,
            progress_logger=progress_logger,
        )
