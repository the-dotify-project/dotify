from re import sub

import click
from cli.types import URL
from cli.ui import echo_dictionary
from cli.views.root import root
from spotify import Playlist


@root.group()
@click.pass_context
def playlist(ctx):
    """Actions on Playlist"""


@playlist.command()
@click.argument('query', type=click.STRING)
@click.option(
    '-l', '--limit',
    default=1, show_default=True,
    type=click.INT, help='search result limit'
)
@click.pass_obj
def search(client, query, limit):
    """Search for a Playlist"""

    results = Playlist.search(client, query, limit=limit)

    for result in results:
        echo_dictionary(result)


@playlist.command()
@click.argument('url', type=URL)
@click.pass_obj
def download(client, url):
    """Download a Playlist"""

    playlist = Playlist.from_url(client, url)

    name = playlist.name
    name = name.strip()
    name = sub(r'\s+', ' ', name)

    playlist.download(name)
