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
@click.pass_obj
def search(client, query, limit):
    """Search for a Track"""

    results = client.Track.search(query, limit=limit)
    results = list(results)

    for result in results:
        echo_dictionary(result)


@track.command()
@click.argument('url', type=URL)
@click.pass_obj
def download(client, url):
    """Download a Track"""

    track = Track.from_url(client, url)

    artist, name = track.artists[0], track.name
    artist, name = artist.strip(), name.strip()
    artist, name = sub(r'\s+', '_', artist), sub(r'\s+', '_', name)

    track.download(f'{artist} - {name}.mp3')
