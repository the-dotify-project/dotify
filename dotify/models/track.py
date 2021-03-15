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
            return [models.Album, models.Artist]

    class InvalidURL(base.Base.InvalidURL):
        pass

    class NotFound(base.Base.NotFound):
        pass

    @property
    def url(self) -> str:
        return self.external_urls.spotify

    def __str__(self):
        return f'{self.artists[0]} - {self.name}'

    def __repr__(self):
        return f'<Track "{self.artists[0]} - {self.name}">'

    #! constructors here are a bit mucky, there are two different constructors for two
    #! different use cases, hence the actual __init__ function does not exist

    #! Note, since the following are class methods, an instance of Track is initialized
    #! and passed to them
    @classmethod
    def from_url(cls, spotify, url: str):
        # FIXME: convert to `Artist`
        # FIXME: less spotify calls (album, artist)

        # check if URL is a playlist, user, artist or album, if yes raise an Exception,
        # else procede
        cls.assert_valid_url(url)

        # query spotify for song, artist, album details
        try:
            raw_track_meta = spotify.client.track(url)
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 404:
                raise cls.NotFound
            elif e.http_status == 400:
                raise cls.InvalidURL
            else:
                raise e

        primary_artist_id = raw_track_meta['artists'][0]['id']
        raw_artist_meta = spotify.client.artist(primary_artist_id)

        album_id = raw_track_meta['album']['id']
        raw_album_meta = spotify.client.album(album_id)

        # get best match from the given provider
        song_name = raw_track_meta['name']

        album_name = raw_track_meta['album']['name']

        duration = round(
            raw_track_meta['duration_ms'] / 1000,
            ndigits=3
        )

        contributing_artists = []

        for artist in raw_track_meta['artists']:
            contributing_artists.append(artist['name'])

        video_search = VideosSearch(
            raw_track_meta['artists'][0]['name'],
            limit=1
        )

        result = video_search.result()

        youtube_link = result['result'][0]['link']

        return Track(
            raw_track_meta, raw_album_meta,
            raw_artist_meta, youtube_link
        )

    @property
    def url_youtube(self) -> str:
        return self.__youtubeLink

    #! Song Details:

    #! 1. Name
    @property
    def name(self) -> str:
        """'
        returns songs's name.
        """

        return self.__rawTrackMeta['name']

    #! 2. Track Number
    @property
    def track_number(self) -> int:
        """
        returns song's track number from album (as in weather its the first
        or second or third or fifth track in the album)
        """

        return self.__rawTrackMeta['track_number']

    #! 3. Genres
    @property
    def genres(self) -> List[str]:
        """
        returns a list of possible genres for the given song, the first member
        of the list is the most likely genre. returns None if genre data could
        not be found.
        """

        return self.__rawAlbumMeta['genres'] + self.__rawArtistMeta['genres']

    #! 4. Duration
    @property
    def duration(self) -> float:
        """
        returns duration of song in seconds.
        """

        return round(self.__rawTrackMeta['duration_ms'] / 1000, ndigits=3)

    #! 5. All involved artists
    @property
    def artists(self) -> List[str]:
        """
        returns a list of all artists who worked on the song.
        The first member of the list is likely the main artist.
        """

        # we get rid of artist name that are in the song title so
        # naming the song would be as easy as
        # $contributingArtists + songName.mp3, we would want to end up with
        # 'Jetta, Mastubs - I'd love to change the world (Mastubs remix).mp3'
        # as a song name, it's dumb.

        contributingArtists = []

        for artist in self.__rawTrackMeta['artists']:
            contributingArtists.append(artist['name'])

        return contributingArtists

    #! Album Details:

    #! 1. Name
    @property
    def album_name(self) -> str:
        """
        returns name of the album that the song belongs to.
        """

        return self.__rawTrackMeta['album']['name']

    #! 2. All involved artist
    @property
    def album_artists(self) -> List[str]:
        """
        returns list of all artists who worked on the album that
        the song belongs to. The first member of the list is likely the main
        artist.
        """

        albumArtists = []

        for artist in self.__rawTrackMeta['album']['artists']:
            albumArtists.append(artist['name'])

        return albumArtists

    #! 3. Release Year/Date
    @property
    def album_release(self) -> str:
        """
        returns date/year of album release depending on what data is available.
        """

        return self.__rawTrackMeta['album']['release_date']

    #! Utilities for genuine use and also for metadata freaks:

    #! 1. Album Art URL
    @property
    def album_cover_url(self) -> str:
        """
        returns url of the biggest album art image available.
        """

        return self.__rawTrackMeta['album']['images'][0]['url']

    #! 2. All the details the spotify-api can provide
    @property
    def dump(self) -> dict:
        """
        returns a dictionary containing the spotify-api responses as-is. The
        dictionary keys are as follows:
            - rawTrackMeta      spotify-api track details
            - rawAlbumMeta      spotify-api song's album details
            - rawArtistMeta     spotify-api song's artist details

        Avoid using this function, it is implemented here only for those super
        rare occasions where there is a need to look up other details. Why
        have to look it up seperately when it's already been looked up once?
        """

        #! internally the only reason this exists is that it helps in saving to disk

        return {
            'youtubeLink': self.__youtubeLink,
            'rawTrackMeta': self.__rawTrackMeta,
            'rawAlbumMeta': self.__rawAlbumMeta,
            'rawArtistMeta': self.__rawArtistMeta
        }

    @property
    def stream(self):
        return YouTube(self.url_youtube).streams.get_audio_only()

    def download(self, path, skip_existing=False):
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
