import html
from os import remove
from os import system as run_in_shell
from pathlib import Path
from typing import List
from urllib.request import urlopen

import dotify.models as models
import dotify.models.base as base
from mutagen.easyid3 import ID3, EasyID3
from mutagen.id3 import APIC as AlbumCover
from pytube import YouTube
from youtubesearchpython import VideosSearch


class Track(base.Base):
    class Json:
        schema = base.Base.Json.schema_dir / 'track.json'

        @classmethod
        def dependencies(cls):
            return [models.Album, models.Artist, models.Image]

    class InvalidURL(base.Base.InvalidURL):
        pass

    class NotFound(base.Base.NotFound):
        pass

    @property
    def url(self) -> str:
        return self.external_urls.spotify

    @property
    def artist(self):
        return self.artists[0]

    def __str__(self):
        return f'{self.artists[0]} - {self.name}'

    def __repr__(self):
        return f'<Track "{str(self)}">'

    @classmethod
    def from_url(cls, url):
        cls.assert_valid_url(url)

        return cls(**cls.get(url))

    @property
    def stream(self):
        video_search = VideosSearch(self.name, limit=1)

        result = video_search.result()

        youtube_url = result['result'][0]['link']

        return YouTube(youtube_url).streams.get_audio_only()

    def download(self, path, skip_existing=False):
        # FIXME: remove, run_in_shell
        # FIXME: genres
        path = Path(path)

        downloaded_file_path = self.stream.download(
            output_path=path.parent,
            filename=path.stem,
            skip_existing=skip_existing
        )

        ffmpeg_cmd = 'ffmpeg -v quiet -y -i "%s" -acodec libmp3lame -abr true -af "apad=pad_dur=2, dynaudnorm, loudnorm=I=-17" "%s"'

        run_in_shell(ffmpeg_cmd % (downloaded_file_path, path))

        # ! Wait till converted file is actually created
        while not path.exists():
            pass

        # ! embed song details
        # ! we save tags as both ID3 v2.3 and v2.4

        # ! The simple ID3 tags
        audio_file = EasyID3(path)

        # ! Get rid of all existing ID3 tags (if any exist)
        audio_file.delete()

        # ! song name
        audio_file['title'] = self.name
        audio_file['titlesort'] = self.name

        # ! track number
        audio_file['tracknumber'] = str(self.track_number)

        # ! genres (pretty pointless if you ask me)
        # ! we only apply the first available genre as ID3 v2.3 doesn't support multiple
        # ! genres and ~80% of the world PC's run Windows - an OS with no ID3 v2.4 support
        genres = self.genres

        if len(genres) > 0:
            audio_file['genre'] = genres[0]

        # ! all involved artists
        audio_file['artist'] = self.artists

        # ! album name
        audio_file['album'] = self.album_name

        # ! album artist (all of 'em)
        audio_file['albumartist'] = self.album_artists

        # ! album release date (to what ever precision available)
        audio_file['date'] = self.album_release
        audio_file['originaldate'] = self.album_release

        # ! save as both ID3 v2.3 & v2.4 as v2.3 isn't fully features and
        # ! windows doesn't support v2.4 until later versions of Win10
        audio_file.save(v2_version=3)

        # ! setting the album art
        audio_file = ID3(path)

        rawAlbumArt = urlopen(self.album_cover_url).read()

        audio_file['APIC'] = AlbumCover(
            encoding=3,
            mime='image/jpeg',
            type=3,
            desc='Cover',
            data=rawAlbumArt
        )

        audio_file.save(v2_version=3)

        # ! delete the unnecessary YouTube download File
        remove(downloaded_file_path)
