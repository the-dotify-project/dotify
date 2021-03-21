from pathlib import Path

import dotify.models as models
from dotify.models.model import Model
from moviepy.editor import AudioFileClip
from mutagen.easyid3 import ID3, EasyID3
from pytube import YouTube
from youtubesearchpython import VideosSearch


class Track(Model):
    class Json:
        schema = Model.Json.schema_dir / 'track.json'

        @classmethod
        def dependencies(cls):
            return [models.Album, models.Artist, models.Image]

    def __str__(self):
        return f'{self.artist} - {self.name}'

    @property
    def url(self) -> str:
        return self.external_urls.spotify

    @property
    def artist(self):
        return self.artists[0]

    @property
    def genres(self):
        genres = []
        for item in [self.album, self.artist]:
            if hasattr(item, 'genres'):
                genres.append(item.genres)

        return genres

    @property
    def genre(self):
        return self.genres[0] if self.genres else None

    def streams(self, limit=1):
        results = VideosSearch(str(self), limit=limit).result()['result']

        for result in results:
            yield YouTube(result['link']).streams.get_audio_only()

    @property
    def stream(self):
        return next(self.streams(limit=1))

    @property
    def id3_tags(self):
        EasyID3.RegisterTextKey('albumcover', 'APIC')

        optional = {}
        if self.genre is not None:
            optional['genre'] = self.genre

        return {
            **optional,
            'title': self.name,
            'titlesort': self.name,
            'tracknumber': str(self.track_number),
            'artist': [artist.name for artist in self.artists],
            'album': self.album.name,
            'albumartist': [artist.name for artist in self.album.artists],
            'date': self.album.release_date,
            'originaldate': self.album.release_date,
            'albumcover': self.album.cover
        }

    def as_mp4(self, mp4_path, skip_existing=False):
        mp4_path = Path(mp4_path)

        return Path(self.stream.download(
            output_path=mp4_path.parent,
            filename=mp4_path.stem,
            skip_existing=skip_existing
        ))

    def as_mp3(self, mp3_path, skip_existing=False, logger=None):
        # FIXME: genres
        # FIXME: progress bar and logging both for moviepy and pytube

        mp3_path = Path(mp3_path)

        mp4_path = self.as_mp4(mp3_path, skip_existing=skip_existing)

        audio_file_clip = AudioFileClip(str(mp4_path))
        audio_file_clip.write_audiofile(str(mp3_path), logger=logger)

        mp4_path.unlink()

        easy_id3 = EasyID3(mp3_path)

        easy_id3.update(self.id3_tags)

        easy_id3.save(v2_version=3)

        return mp3_path

    def download(self, mp3_path, skip_existing=False, logger=None):
        return self.as_mp3(mp3_path, skip_existing=skip_existing, logger=logger)

    @classmethod
    @Model.validate_url
    @Model.convert_to_model_error
    def from_url(cls, url):
        return cls(**cls.client.track(url))
