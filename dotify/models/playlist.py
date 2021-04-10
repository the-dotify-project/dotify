import logging
from os import PathLike
from pathlib import Path
from typing import TYPE_CHECKING, Iterator

import dotify.models as models
from dotify.model import Model, logger

logger = logging.getLogger(f"{logger.name}.{__name__}")

if TYPE_CHECKING is True:
    from dotify.models.track import Track


class Playlist(Model):
    """ """

    class Json:
        """ """

        dependencies = ["dotify.models.User", "dotify.models.Image"]

    def __init__(self, **props) -> None:
        if "tracks" in props:
            del props["tracks"]

        super().__init__(**props)

    def __str__(self):
        return self.name

    def __iter__(self):
        return self.tracks

    @property
    def url(self):
        """ """
        return self.external_urls.spotify

    @property
    def tracks(self) -> Iterator["Track"]:
        """ """
        response, offset = (
            self.context.playlist_items(self.url, additional_types=("track",)),
            0,
        )

        while True:
            for result in response["items"]:
                url = result["track"]["external_urls"]["spotify"]

                yield models.Track.from_url(url)

            offset += len(response["items"])

            if response["next"] is None:
                break

            response = self.context.playlist_items(
                self.url, additional_types=("track",), offset=offset
            )

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
    def from_url(cls, url: str) -> "Playlist":
        """"""
        return cls(**cls.context.playlist(url))
