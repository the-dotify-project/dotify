
import json
from pathlib import Path

DOTIFY_SETTINGS = json.load((Path.cwd() / 'api' / 'settings.json').open())
