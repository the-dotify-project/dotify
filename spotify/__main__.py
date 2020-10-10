
from spotify.provider import Spotify
from spotify.settings import DEFAULT

if __name__ == "__main__":
    # with Spotify(SPOTIFY) as provider:
    #     rv = provider.download_track('https://open.spotify.com/track/691df0fYjhhszUgQH3FGvP?si=IaDHTfJFTmiJIcos2MjzWg')
    #     print(rv)

    # with Spotify(SPOTIFY) as provider:
    #     rv = provider.download_album('https://open.spotify.com/album/0ufGvePLRPce9olVIZhRyE?si=H_LVsESVT1OhIyT9oT86Qg')
    #     print(rv)

    # with Spotify(SPOTIFY) as provider:
    #     searcher = MetadataSearch(
    #         'https://open.spotify.com/track/691df0fYjhhszUgQH3FGvP',
    #     )

    #     metadata = searcher.on_youtube_and_spotify()

    #     from pprint import pprint
    #     pprint(metadata)

    # with Spotify(SPOTIFY) as provider:
    #     provider.download_track_from_metadata(
    #         {
    #             "name": "94 Bentley",
    #             "album": {
    #                 "name": "Ghetto Lenny's Love Songs",
    #                 "external_urls": {
    #                     "spotify": "https://open.spotify.com/album/0ufGvePLRPce9olVIZhRyE?si=H_LVsESVT1OhIyT9oT86Qg"
    #                 },
    #                 "images": [
    #                     {
    #                         "url": "https://i.scdn.co/image/ab67616d0000b273cdb624d3049740537b9f7b50"
    #                     }
    #                 ],
    #             },
    #             "artists": [
    #                 {
    #                     "name": "SAINt JHN",
    #                     "external_urls": {
    #                         "spotfiy": "https://open.spotify.com/artist/0H39MdGGX6dbnnQPt6NQkZ"
    #                     },
    #                 }
    #             ],
    #             "external_urls": {
    #                 "spotify": "https://open.spotify.com/track/691df0fYjhhszUgQH3FGvP"
    #             },
    #         }
    #     )

    with Spotify() as spotify:
        print(
            spotify.fetch_playlist(
                "https://open.spotify.com/playlist/7LleICaPbgvmwh9GExnbOY?si=5utOlLCKTMWVpZmFlOGf2A"
            )
        )
