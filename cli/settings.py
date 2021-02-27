
import json
from pathlib import Path

DOTIFY_SETTINGS = json.load((Path(__file__).parent / 'settings.json').open())
