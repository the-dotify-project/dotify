import logging
from pathlib import Path
from typing import TYPE_CHECKING, AnyStr, Iterator, Optional, cast

import dotify
from dotify._model import Model, logger

logger = logging.getLogger("{0}.{1}".format(logger.name, __name__))

if TYPE_CHECKING is True:
    from dotify.models._track import Track


class PlaylistBase(Model):
    """`PlaylistBase` defines the interface of the Playlist class, which is subclassing it."""

    class Json(object):
        abstract = True

    def __init__(self, **props) -> None:  # noqa: D107
        props.pop("tracks", None)

        super().__init__(**props)

    def __str__(self):
        return self.name

    def __iter__(self):
        return self.tracks

    @property
    def url(self) -> AnyStr:
        """Return the playlist's Spotify URL.

        Returns:
            AnyStr: the URL in string format
        """
        return cast(AnyStr, self.external_urls.spotify)

    @property
    def tracks(self) -> Iterator["Track"]:
        """Return the playlist tracks.

        Yields:
            Iterator["Track"]: the playlist tracks
        """
        response, offset = (
            self.context.playlist_items(self.url, additional_types=("track",)),
            0,
        )

        while True:
            for result in response["items"]:
                url = result["track"]["external_urls"]["spotify"]

                yield dotify.models._track.Track.from_url(url)

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
    def from_url(cls, url: AnyStr) -> "Playlist":
        """Return a `Playlist` given its corresponding Spotify URL.

        Args:
            url (AnyStr): the Spotify URL of the playlist

        Returns:
            Playlist: the corresponding playlist
        """
        return cls(**cls.context.playlist(url))


class Playlist(PlaylistBase):
    """`Playlist` implements the playlist downloading logic."""

    class Json(object):
        dependencies = ["dotify.models.User", "dotify.models.Image"]

    def download(
        self,
        path: Path,
        skip_existing: Optional[bool] = False,
        progress_logger: Optional[logging.Logger] = None,
    ) -> Path:
        """Download the playlist's tracks in `.mp3` format.

        Args:
            path (Path): where should the tracks be stored
            skip_existing (Optional[bool]): whether or not to overwrite an
                existing track. Defaults to False.
            progress_logger (Optional[logging.Logger]): a logger reporting
                on the download progress. Defaults to None.

        Returns:
            Path: the download folder of the playlist
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
