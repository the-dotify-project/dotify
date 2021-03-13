from pathlib import Path

from dotify.json_serializable import JsonSerializable


class Artist(JsonSerializable):
    class Json:
        schema = schema = Path(__file__).parent / 'schema' / 'artist.json'
