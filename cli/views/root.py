import cli
import click
from cli.settings import DOTIFY_SETTINGS
from spotify.provider import Spotify


@click.group()
@click.pass_context
def root(ctx):
    client = Spotify(DOTIFY_SETTINGS['spotify_id'], DOTIFY_SETTINGS['spotify_secret'])
    client.connect()

    ctx.obj = client
