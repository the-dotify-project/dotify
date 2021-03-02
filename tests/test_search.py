from spotify import Album, Playlist, Track

from tests.base import DotifyBaseTestCase


class DotifySearchTestCase(DotifyBaseTestCase):
    def test_search_track(self):
        metadata = {
            'url': 'https://open.spotify.com/track/0fFWxRZGKR7HDW2xBMOZgW',
            'name': '5 Thousand Singles',
            'album': {
                'name': "Ghetto Lenny's Love Songs",
                'url': 'https://open.spotify.com/album/0ufGvePLRPce9olVIZhRyE',
                'images': [
                    {
                        'height': 640,
                        'url': 'https://i.scdn.co/image/ab67616d0000b273cdb624d3049740537b9f7b50',
                        'width': 640
                    },
                    {
                        'height': 300,
                        'url': 'https://i.scdn.co/image/ab67616d00001e02cdb624d3049740537b9f7b50',
                        'width': 300
                    },
                    {
                        'height': 64,
                        'url': 'https://i.scdn.co/image/ab67616d00004851cdb624d3049740537b9f7b50',
                        'width': 64
                    }
                ],
                'artist': {
                    'name': 'SAINt JHN',
                    'url': 'https://open.spotify.com/artist/0H39MdGGX6dbnnQPt6NQkZ'
                }
            }
        }

        self.search(Track, metadata['name'], metadata)

    def test_search_playlist(self):
        metadata = {
            'description': '',
            'images': [
                {
                    'height': 640,
                    'url': 'https://mosaic.scdn.co/640/ab67616d0000b273a464531ee45ed8aa42eb54bfab67616d0000b273b57d9a7441b74f1c8debe51eab67616d0000b273bd320edc480061c161bb6285ab67616d0000b273c8e0d481bba8b6c47e1a54f2',
                    'width': 640
                },
                {
                    'height': 300,
                    'url': 'https://mosaic.scdn.co/300/ab67616d0000b273a464531ee45ed8aa42eb54bfab67616d0000b273b57d9a7441b74f1c8debe51eab67616d0000b273bd320edc480061c161bb6285ab67616d0000b273c8e0d481bba8b6c47e1a54f2',
                    'width': 300},
                {
                    'height': 60,
                    'url': 'https://mosaic.scdn.co/60/ab67616d0000b273a464531ee45ed8aa42eb54bfab67616d0000b273b57d9a7441b74f1c8debe51eab67616d0000b273bd320edc480061c161bb6285ab67616d0000b273c8e0d481bba8b6c47e1a54f2',
                    'width': 60
                }
            ],
            'name': 'Playlist Ninho',
            'url': 'https://open.spotify.com/playlist/6A5oPdsnxqQVhpBhba8hXR'
        }

        self.search(Playlist, metadata['name'], metadata)

    def test_search_album(self):
        metadata = {
            'artist': {
                'name': 'Eminem',
                'url': 'https://open.spotify.com/artist/7dGJo4pcD2V6oG8kP0tJRR'
            },
            'images': [
                {
                    'height': 640,
                    'url': 'https://i.scdn.co/image/ab67616d0000b273b84b0516d901f95461bb5165',
                    'width': 640
                },
                {
                    'height': 300,
                    'url': 'https://i.scdn.co/image/ab67616d00001e02b84b0516d901f95461bb5165',
                    'width': 300
                },
                {
                    'height': 64,
                    'url': 'https://i.scdn.co/image/ab67616d00004851b84b0516d901f95461bb5165',
                    'width': 64
                }
            ],
            'name': 'Music To Be Murdered By - Side B (Deluxe Edition)',
            'url': 'https://open.spotify.com/album/3MKvhQoFSrR2PrxXXBHe9B'
        }

        self.search(Album, metadata['name'], metadata)
