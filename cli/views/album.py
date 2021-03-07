import html
from pprint import pprint
from re import sub

import click
from cli.types import URL
from cli.ui import echo_dictionary
from cli.views.root import root
from dotify import Album


@root.group()
@click.pass_context
def album(ctx):
    """Actions on Albums"""


@album.command()
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
    """Search for an Album"""

    results = client.Album.search(query, limit=limit)

    for result in results:
        result = {
            "url": result.url,
            "name": html.unescape(str(result.name).strip()),
            "artist": {
                "name": html.unescape(str(result.artist.name).strip()),
                "url": result.artist.external_urls.spotify,
            },
            "images": [{
                'url': image.url,
                'height': image.height,
                'width': image.width
            }
                for image in result.images
            ]
        }

        if raw is True:
            pprint(result, indent=4)
            continue

        echo_dictionary(result)


@album.command()
@click.argument('url', type=URL)
@click.pass_obj
def download(client, url):
    """Download an Album"""

    album = Album.from_url(client, url)

    artist, name = album.artist.name, album.name
    artist, name = artist.strip(), name.strip()
    artist, name = sub(r'\s+', ' ', artist), sub(r'\s+', ' ', name)

    album.download(f'{artist} - {name}')
