"""Yet another Spotify Web API Python library.

Examples:
---
    >>> from dotify import Dotify, Track
    >>> with Dotify(SPOTIFY_ID, SPOTIFY_SECRET):
    >>>     result = next(Track.search("SAINt JHN 5 Thousand Singles", limit=1))
    >>> result
    <Track "SAINt JHN - 5 Thousand Singles">
    >>> result.url
    'https://open.spotify.com/track/0fFWxRZGKR7HDW2xBMOZgW'
    >>> result.download("SAINt JHN - 5 Thousand Singles.mp3")
    PosixPath('SAINt JHN - 5 Thousand Singles.mp3')
"""

__all__ = [
    "Dotify",
]

from dotify._dotify import Dotify
