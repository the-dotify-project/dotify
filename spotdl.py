
from pathlib import Path

import click

from spotify import Album, Playlist, Track
from cli import URL
from spotify.provider import Spotify
from cli import root
from pprint import pprint

SETTINGS = {
    'client_id': 'baecc053210f454999f9723da1631f35',
    'client_secret': '7c34bec415e34b13ad56dcee8475005a'
}

ID, SECRET = SETTINGS['client_id'], SETTINGS['client_secret']

if __name__ == "__main__":
    root()
    # FIXME: python spotdl.py track download "https://open.spotify.com/track/691df0fYjhhszUgQH3FGvP?si=IaDHTfJFTmiJIcos2MjzWg"

    with Spotify(ID, SECRET) as spotify:
        #     meta = spotify.client.track(
        #         'https://open.spotify.com/track/691df0fYjhhszUgQH3FGvP?si=IaDHTfJFTmiJIcos2MjzWg'
        #     )

        #     pprint(meta)

        #     pprint(meta)

        #     exit()

        #     #     print()
        #     # pprint(spotify.tracks_of_album(
        #     #     'https://open.spotify.com/album/0ufGvePLRPce9olVIZhRyE?si=exyyslsCS0m9HcVgIxUOjg'
        #     # ))

        # url = next(spotify.search_track("Left Hand Free"))['url']
        # 'https://open.spotify.com/track/1Gkuz8ggxpZmfm7HSAc2qI'
        url = 'https://open.spotify.com/album/5WEwObchJdvIzPcmm2e3Li'
        album = spotify.album_from_url(url)

        print(album)

        # pprint(track.dump['rawTrackMeta']['external_urls']['spotify'])

        artist = album.artist.name
        name = album.name

        path = Path(f'{artist} - {name}')

        print(path)

        album.download(path)

    #     # url = spotify.search_album("Ghetto Lenny's Love Songs")[0]['url']
    #     # url = "https://open.spotify.com/playlist/1HkE7QDzcdtF3lQGVF744N?si=T9Spnl9mSXuUTzI90zyQAg"

    #     # path = Path.cwd() / 'Lenny'

    #     # spotify.download_playlist(url, path)
