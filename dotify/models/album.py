import logging
from http import HTTPStatus
from os import PathLike
from pathlib import Path
from typing import Any, Iterator

import requests
from mutagen.id3 import APIC

import dotify
from dotify.model import Model, logger

logger = logging.getLogger("{0}.{1}".format(logger.name, __name__))


class AlbumBase(Model):
    """ """

    def __str__(self):
        return "{0} - {1}".format(self.artist, self.name)

    def __iter__(self):
        return self.tracks

    @property
    def artist(self) -> "dotify.models.artist.Artist":
        """ """
        return self.artists[0]

    @property
    def url(self):
        """ """
        return self.external_urls.spotify

    @property
    def cover(self) -> Any:
        """ """
        response = requests.get(self.images[0].url)

        if response.status_code != HTTPStatus.OK.value:
            raise ConnectionError(
                "Failed to fetch {0}".format(
                    self.images[0].url,
                ),
            )

        return APIC(
            encoding=3,
            mime="image/jpeg",
            type=3,
            desc="Cover",
            data=response.content,
        )

    @property
    def tracks(self) -> Iterator["dotify.models.track.Track"]:
        """ """
        response, offset = self.context.album_tracks(self.url), 0

        while True:
            for result in response["items"]:
                url = result["external_urls"]["spotify"]

                yield dotify.models.track.Track.from_url(url)

            offset += len(response["items"])

            if response["next"] is None:
                break

            response = self.context.album_tracks(self.url, offset=offset)

    @classmethod
    @Model.validate_url
    @Model.http_safeguard
    def from_url(cls, url: str) -> "dotify.models.album.Album":
        """ """
        return cls(**cls.context.album(url))


class Album(AlbumBase):
    class Json(object):
        """ """

        dependencies = [
            "dotify.models.Track",
            "dotify.models.Artist",
            "dotify.models.Image",
        ]

    def download(
        self,
        path: PathLike,
        skip_existing: bool = False,
        progress_logger: None = None,
    ) -> PathLike:
        """ """
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
