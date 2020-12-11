import cli
import click
from cli.settings import SETTINGS
from spotify.provider import Spotify


@click.group()
@click.pass_context
def root(ctx):
    client = Spotify(SETTINGS['client_id'], SETTINGS['client_secret'])
    client.connect()

    ctx.obj = client
