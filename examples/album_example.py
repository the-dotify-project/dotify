from dotify import Dotify, models

if __name__ == "__main__":
    with Dotify():
        album = next(models.Album.search("SAINt JHN Ghetto Lenny's Love Songs", limit=1))

        for track in album:
            print(track)

        print(album)

        album = models.Album.from_url("https://open.spotify.com/album/5WEwObchJdvIzPcmm2e3Li")

        print(album)

        album.download(str(album))
