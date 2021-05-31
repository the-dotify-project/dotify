import logging
from os import PathLike
from pathlib import Path
from typing import Iterator

import dotify
from dotify.model import Model, logger

logger = logging.getLogger("{0}.{1}".format(logger.name, __name__))


class PlaylistBase(Model):
    """ """

    def __init__(self, **props) -> None:
        props.pop("tracks", None)

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
    def tracks(self) -> Iterator["dotify.models.track.Track"]:
        """ """
        response, offset = (
            self.context.playlist_items(self.url, additional_types=("track",)),
            0,
        )

        while True:
            for result in response["items"]:
                url = result["track"]["external_urls"]["spotify"]

                yield dotify.models.track.Track.from_url(url)

            offset += len(response["items"])

            if response["next"] is None:
                break

            response = self.context.playlist_items(
                self.url,
                additional_types=("track",),
                offset=offset,
            )

    @classmethod
    @Model.validate_url
    @Model.http_safeguard
    def from_url(cls, url: str) -> "Playlist":
        """ """
        return cls(**cls.context.playlist(url))


class Playlist(PlaylistBase):
    class Json(object):
        """ """

        dependencies = ["dotify.models.User", "dotify.models.Image"]

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
