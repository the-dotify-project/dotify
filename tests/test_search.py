from tests.base import DotifyBaseTestCase


class DotifySearchTestCase(DotifyBaseTestCase):
    def test_search_track(self):
        metadata = [
            {
                "name": "5 Thousand Singles",
                "url": "https://open.spotify.com/track/0fFWxRZGKR7HDW2xBMOZgW",
                "album.name": "Ghetto Lenny's Love Songs",
                "album.url": "https://open.spotify.com/album/0ufGvePLRPce9olVIZhRyE",
                "artist.name": "SAINt JHN",
                "artist.url": "https://open.spotify.com/artist/0H39MdGGX6dbnnQPt6NQkZ",
            },
        ]

        self.search("Track", metadata[0]["name"], metadata)

    def test_search_playlist(self):
        metadata = [
            {
                "name": "Richard's Moustache",
                "url": "https://open.spotify.com/playlist/4EMku5bJCeA1lG9Y8oThrs",
                "description": "the weirdest name for a playlist with the best songs",
            },
        ]

        self.search("Playlist", metadata[0]["name"], metadata)

    def test_search_album(self):
        metadata = [
            {
                "name": "Music To Be Murdered By - Side B (Deluxe Edition)",
                "url": "https://open.spotify.com/album/3MKvhQoFSrR2PrxXXBHe9B",
                "artist.name": "Eminem",
                "artist.url": "https://open.spotify.com/artist/7dGJo4pcD2V6oG8kP0tJRR",
            },
        ]

        self.search("Album", metadata[0]["name"], metadata)
