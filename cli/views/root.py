import cli
import click
from cli.settings import DOTIFY_SETTINGS
from dotify.dotify import Dotify


@click.group()
@click.pass_context
def root(ctx):
    client = Dotify(
        DOTIFY_SETTINGS['spotify_id'],
        DOTIFY_SETTINGS['spotify_secret']
    )

    ctx.obj = client
