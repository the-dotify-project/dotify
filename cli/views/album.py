from re import sub

import click
from cli.types import URL
from cli.ui import echo_dictionary
from cli.views.root import root
from spotify import Album


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
@click.pass_obj
def search(client, query, limit):
    """Search for an Album"""

    results = Album.search(client, query, limit=limit)

    for result in results:
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
