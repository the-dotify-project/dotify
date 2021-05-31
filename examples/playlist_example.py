import os

from dotify import Dotify, Playlist

if __name__ == "__main__":
    SPOTIFY_ID = os.environ.get("SPOTIFY_ID")
    SPOTIFY_SECRET = os.environ.get("SPOTIFY_SECRET")

    with Dotify(SPOTIFY_ID, SPOTIFY_SECRET):
        playlist = next(Playlist.search("RapCaviar", limit=1))

        for track in playlist:
            print(track)

        print(playlist)
        playlist = Playlist.from_url(
            "https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd",
        )
        print(playlist)
        playlist.download(str(playlist))
