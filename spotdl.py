from cli import root
from spotipy import Spotify, SpotifyClientCredentials
from cli.settings import DOTIFY_SETTINGS
from pprint import pprint
from python_jsonschema_objects import ObjectBuilder
from pathlib import Path
from json import load

if __name__ == '__main__':
    root()

    with Path('/mnt/c/Users/bills/Desktop/dotify/dotify-backend/dotify/models/schema/album.json').open() as file:
        schema = load(file)

        pprint(schema)

        builder = ObjectBuilder(schema)
        classes = builder.build_classes(
            strict=True,
            named_only=True,
            standardize_names=False
        )

    album = classes.Album(**{'album_type': 'single', 'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/3XHO7cRUPCLOr6jwp8vsx5'}, 'href': 'https://api.spotify.com/v1/artists/3XHO7cRUPCLOr6jwp8vsx5', 'id': '3XHO7cRUPCLOr6jwp8vsx5', 'name': 'alt-J', 'type': 'artist', 'uri': 'spotify:artist:3XHO7cRUPCLOr6jwp8vsx5'}], 'available_markets': ['CA', 'MX', 'US'], 'external_urls': {'spotify': 'https://open.spotify.com/album/1TtL3hpXpw9ymcqU0Gewvt'}, 'href': 'https://api.spotify.com/v1/albums/1TtL3hpXpw9ymcqU0Gewvt', 'id': '1TtL3hpXpw9ymcqU0Gewvt', 'images': [
        {'height': 640, 'url': 'https://i.scdn.co/image/ab67616d0000b2736a48591a72e51b31618f6eff', 'width': 640}, {'height': 300, 'url': 'https://i.scdn.co/image/ab67616d00001e026a48591a72e51b31618f6eff', 'width': 300}, {'height': 64, 'url': 'https://i.scdn.co/image/ab67616d000048516a48591a72e51b31618f6eff', 'width': 64}], 'name': 'Left Hand Free (Lido Remix)', 'release_date': '2014-10-27', 'release_date_precision': 'day', 'total_tracks': 1, 'type': 'album', 'uri': 'spotify:album:1TtL3hpXpw9ymcqU0Gewvt'})

    print(album.artists[0])

    # credential_manager = SpotifyClientCredentials(
    #     client_id=DOTIFY_SETTINGS['spotify_id'],
    #     client_secret=DOTIFY_SETTINGS['spotify_secret']
    # )

    # print(credential_manager.get_access_token())

    # client = Spotify(
    #     client_credentials_manager=credential_manager
    # )

    # results = client.search('5 Thousand Signles', type='track', limit=1)

    # # pprint(results)
