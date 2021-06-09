import os

from dotify import Dotify, models

if __name__ == "__main__":
    SPOTIFY_ID = os.environ.get("SPOTIFY_ID")
    SPOTIFY_SECRET = os.environ.get("SPOTIFY_SECRET")

    with Dotify(SPOTIFY_ID, SPOTIFY_SECRET):
        album = next(
            models.Album.search("SAINt JHN Ghetto Lenny's Love Songs", limit=1)
        )

        for track in album:
            print(track)

        print(album)

        album = models.Album.from_url(
            "https://open.spotify.com/album/0ufGvePLRPce9olVIZhRyE"
        )

        print(album)

        album.download(str(album))
