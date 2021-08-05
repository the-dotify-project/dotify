import logging
from http import HTTPStatus
from pathlib import Path
from typing import TYPE_CHECKING, AnyStr, Iterator, Optional, cast

import requests
from cached_property import cached_property
from mutagen.id3 import APIC
from requests.models import HTTPError

import dotify
from dotify._model import Model, logger

logger = logging.getLogger("{0}.{1}".format(logger.name, __name__))

if TYPE_CHECKING is True:
    from dotify.models._artist import Artist
    from dotify.models._track import Track


class AlbumBase(Model):
    """`AlbumBase` defines the interface of the Album class, which is subclassing it."""

    class Json(object):
        abstract = True

    def __str__(self):
        return "{0} - {1}".format(self.artist, self.name)

    def __iter__(self):
        return self.tracks

    @property
    def artist(self) -> "Artist":
        """Return the album's artist.

        Returns:
            Artist: an instance of `Artist` representing the album's artist relevant info
        """
        return cast("Artist", self.artists[0])

    @property
    def url(self) -> AnyStr:
        """Return the album's Spotify URL.

        Returns:
            AnyStr: the URL in string format
        """
        return cast(AnyStr, self.external_urls.spotify)

    @cached_property
    def cover(self) -> APIC:
        """Return the cover art of the album.

        Raises:
            HTTPError: if response status code is indicative of an error

        Returns:
            APIC: the album's cover
        """
        response = requests.get(self.images[0].url)

        if response.status_code != HTTPStatus.OK.value:
            raise HTTPError(
                "Failed to fetch %s" % (self.images[0].url,),
                response=response,
            )

        return APIC(
            encoding=3,
            mime="image/jpeg",
            type=3,
            desc="Cover",
            data=response.content,
        )

    @property
    def tracks(self) -> Iterator["Track"]:
        """Return the album tracks.

        Yields:
            Iterator["Track"]: the album tracks
        """
        response, offset = self.context.album_tracks(self.url), 0

        while True:
            for result in response["items"]:
                url = result["external_urls"]["spotify"]

                yield dotify.models._track.Track.from_url(url)

            offset += len(response["items"])

            if response["next"] is None:
                break

            response = self.context.album_tracks(self.url, offset=offset)

    @classmethod
    @Model.validate_url
    @Model.http_safeguard
    def from_url(cls, url: AnyStr) -> "Album":
        """Return an `Album` given its corresponding Spotify URL.

        Args:
            url (AnyStr): the Spotify URL of the album

        Returns:
            Album: the corresponding album
        """
        return cls(**cls.context.album(url))


class Album(AlbumBase):
    """`Album` implements the album downloading logic."""

    class Json(object):
        dependencies = [
            "dotify.models.Track",
            "dotify.models.Artist",
            "dotify.models.Image",
        ]

    def download(
        self,
        path: Path,
        skip_existing: Optional[bool] = False,
        progress_logger: Optional[logging.Logger] = None,
    ) -> Path:
        """Download the album's tracks in `.mp3` format.

        Args:
            path (Path): where should the tracks be stored
            skip_existing (Optional[bool]): whether or not to overwrite an
                existing track. Defaults to False
            progress_logger (Optional[logging.Logger]): a logger reporting on
                the download progress. Defaults to None.

        Returns:
            Path: the download folder of the album
        """
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)

        for track in self.tracks:
            track.download(
                path
                / "{0}.mp3".format(
                    track,
                ),
                skip_existing=skip_existing,
                progress_logger=progress_logger,
            )

        return path
