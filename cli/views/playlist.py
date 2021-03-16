import html
from pprint import pprint
from re import sub

import click
from cli.types import URL
from cli.ui import echo_dictionary
from cli.views.root import root
from dotify import Playlist


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
@click.option(
    '-r', '--raw',
    default=False, show_default=True,
    is_flag=True, help='output a dictionary'
)
@click.pass_obj
def search(client, query, limit, raw):
    """Search for a Playlist"""

    results = client.Playlist.search(query, limit=limit)

    for result in results:
        result = {
            'url': result.url,
            'name': html.unescape(result.name).strip(),
            'description': html.unescape(result.description).strip(),
            'images': result.images
        }

        echo_dictionary(result) if not raw else pprint(result, indent=4)


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
