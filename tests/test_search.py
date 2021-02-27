from tests.base import DotifyBaseTestCase

class DotifySearchTestCase(DotifyBaseTestCase):
    def test_search_track(self):
        metadata = [{'url': 'https://open.spotify.com/track/0fFWxRZGKR7HDW2xBMOZgW', 'name': '5 Thousand Singles', 'album': {'name': "Ghetto Lenny's Love Songs", 'url': 'https://open.spotify.com/album/0ufGvePLRPce9olVIZhRyE', 'images': [{'height': 640, 'url': 'https://i.scdn.co/image/ab67616d0000b273cdb624d3049740537b9f7b50', 'width': 640}, {'height': 300, 'url': 'https://i.scdn.co/image/ab67616d00001e02cdb624d3049740537b9f7b50', 'width': 300}, {'height': 64, 'url': 'https://i.scdn.co/image/ab67616d00004851cdb624d3049740537b9f7b50', 'width': 64}], 'artist': {'name': 'SAINt JHN', 'url': 'https://open.spotify.com/artist/0H39MdGGX6dbnnQPt6NQkZ'}}}]

        self.download_track(url)

    def test_search_playlist(self):
        url = 'https://open.spotify.com/playlist/1HkE7QDzcdtF3lQGVF744N'
        self.download_playlist(url)

    def test_search_album(self):
        url = 'https://open.spotify.com/album/5WEwObchJdvIzPcmm2e3Li'
        self.download_album(url)
