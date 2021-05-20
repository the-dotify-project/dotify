import os

DOTIFY_SETTINGS = (
    os.environ.get("SPOTIFY_ID"),
    os.environ.get("SPOTIFY_SECRET"),
)

if DOTIFY_SETTINGS[0] is None:
    raise AssertionError("Failed to retrieve Spotify API ID")

if DOTIFY_SETTINGS[0] is None:
    raise AssertionError("Failed to retrieve Spotify API Secret")
