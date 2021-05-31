import contextlib
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List
from urllib.error import HTTPError

from moviepy.editor import AudioFileClip
from mutagen.easyid3 import EasyID3
from pytube import YouTube
from pytube.streams import Stream
from youtubesearchpython import VideosSearch

from dotify.model import Model, logger

logger = logging.getLogger("{0}.{1}".format(logger.name, __name__))

EasyID3.RegisterTextKey("albumcover", "APIC")

if TYPE_CHECKING is True:
    from dotify.models.artist import Artist


class TrackBase(Model):
    """ """

    def __str__(self) -> str:
        return "{0} - {1}".format(self.artist, self.name)

    @property
    def url(self) -> str:
        """ """
        return self.external_urls.spotify

    @property
    def artist(self) -> "Artist":
        """ """
        return self.artists[0]

    @property
    def genres(self) -> List[Any]:
        """ """
        genres = []
        for item in (self.album, self.artist):
            with contextlib.suppress(AttributeError):
                genres.append(item.genres)

        return genres

    @property
    def genre(self) -> None:
        """ """
        return self.genres[0] if self.genres else None

    @classmethod
    @Model.validate_url
    @Model.http_safeguard
    def from_url(cls, url: str) -> "Track":
        """ """
        return cls(**cls.context.track(url))


class Track(TrackBase):
    class Json(object):
        """ """

        dependencies = [
            "dotify.models.Album",
            "dotify.models.Artist",
            "dotify.models.Image",
        ]

    def streams(self, limit=1):
        """ """
        results = VideosSearch(str(self), limit=limit).result()["result"]

        yield from (
            YouTube(result["link"]).streams.get_audio_only() for result in results
        )

    @property
    def stream(self) -> Stream:
        """ """
        return next(self.streams(limit=1))

    @property
    def id3_tags(self) -> Dict[str, Any]:
        """ """
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

    def as_mp4(self, mp4_path: Path, skip_existing: bool = False) -> Path:
        """ """
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
        skip_existing: bool = False,
        progress_logger: None = None,
    ) -> Path:
        """ """
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
        skip_existing: bool = False,
        progress_logger: None = None,
    ) -> Path:
        """ """
        return self.as_mp3(
            mp3_path,
            skip_existing=skip_existing,
            progress_logger=progress_logger,
        )
