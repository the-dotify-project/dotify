import html
from pprint import pprint
from re import sub

import click
from cli.types import URL
from cli.ui import echo_dictionary
from cli.views.root import root
from dotify import Track


@root.group()
@click.pass_context
def track(ctx):
    """Actions on Tracks"""


@track.command()
@click.argument('query', type=click.STRING)
@click.option(
    '-l', '--limit',
    default=1, show_default=True,
    type=click.INT, help='search result limit'
)
@click.option(
    '-r', '--raw',
    default=False, show_default=True,
    is_flag=True, help='output a dictionary'
)
@click.pass_obj
def search(client, query, limit, raw):
    """Search for a Track"""

    results = client.Track.search(query, limit=limit)
    results = list(results)

    for result in results:
        result = {
            "url": result.url,
            "name": html.unescape(result.name).strip(),
            "album": {
                "name": html.unescape(result.album.name).strip(),
                "url": result.album.external_urls.spotify,
                "images": result.album.images,
                "artist": html.unescape(result.artist.name).strip()
            }
        }

        echo_dictionary(result) if not raw else pprint(result, indent=4)


@track.command()
@click.argument('url', type=URL)
@click.pass_obj
def download(client, url):
    """Download a Track"""

    track = client.Track.from_url(url)

    artist, name = track.artist.name, track.name
    artist, name = artist.strip(), name.strip()
    artist, name = sub(r'\s+', '_', artist), sub(r'\s+', '_', name)

    track.as_mp3(f'{artist} - {name}.mp3')
