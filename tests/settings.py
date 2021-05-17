import json
import os
from pathlib import Path

SETTINGS_PATH = Path(__file__).parent.parent / "settings.json"

if SETTINGS_PATH.is_file():
    with SETTINGS_PATH.open() as file:
        DOTIFY_SETTINGS = json.load(file)
else:
    DOTIFY_SETTINGS = {
        "spotify_id": os.environ.get("SPOTIFY_ID"),
        "spotify_secret": os.environ.get("SPOTIFY_SECRET"),
    }

if DOTIFY_SETTINGS["spotify_id"] is None:
    raise AssertionError("Failed to retrieve Spotify API ID")

if DOTIFY_SETTINGS["spotify_secret"] is None:
    raise AssertionError("Failed to retrieve Spotify API Secret")
