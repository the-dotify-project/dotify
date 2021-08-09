from dotify import Dotify, models

if __name__ == "__main__":
    with Dotify():
        playlist = next(models.Playlist.search("RapCaviar", limit=1))

        for track in playlist:
            print(track)

        print(playlist)

        playlist = models.Playlist.from_url(
            "https://open.spotify.com/playlist/1HkE7QDzcdtF3lQGVF744N",
        )

        print(playlist)

        playlist.download(str(playlist))
