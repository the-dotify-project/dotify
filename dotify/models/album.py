import logging
from os import PathLike
from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterator

import requests
from mutagen.id3 import APIC

import dotify.models as models
from dotify.model import Model, logger

logger = logging.getLogger(f"{logger.name}.{__name__}")

if TYPE_CHECKING is True:
    from dotify.models.artist import Artist
    from dotify.models.track import Track


class Album(Model):
    """ """

    class Json:
        """ """

        dependencies = [
            "dotify.models.Track",
            "dotify.models.Artist",
            "dotify.models.Image",
        ]

    def __str__(self):
        return f"{self.artist} - {self.name}"

    def __iter__(self):
        return self.tracks

    @property
    def artist(self) -> "Artist":
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

        assert response.status_code == 200, f"Failed to fetch {self.images[0].url}"

        return APIC(
            encoding=3, mime="image/jpeg", type=3, desc="Cover", data=response.content
        )

    @property
    def tracks(self) -> Iterator["Track"]:
        """ """
        response, offset = self.context.album_tracks(self.url), 0

        while True:
            for result in response["items"]:
                url = result["external_urls"]["spotify"]

                yield models.Track.from_url(url)

            offset += len(response["items"])

            if response["next"] is None:
                break

            response = self.context.album_tracks(self.url, offset=offset)

    def download(
        self, path: PathLike, skip_existing: bool = False, logger: None = None
    ) -> PathLike:
        """"""
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)

        for track in self.tracks:
            track.download(
                path / f"{track}.mp3", skip_existing=skip_existing, logger=logger
            )

        return path

    @classmethod
    @Model.validate_url
    @Model.http_safeguard
    def from_url(cls, url: str) -> "Album":
        """"""
        return cls(**cls.context.album(url))
