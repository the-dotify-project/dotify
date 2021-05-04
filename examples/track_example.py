import os

from dotify import Dotify, Track

if __name__ == "__main__":
    SPOTIFY_ID = os.environ.get("SPOTIFY_ID")
    SPOTIFY_SECRET = os.environ.get("SPOTIFY_SECRET")

    with Dotify(SPOTIFY_ID, SPOTIFY_SECRET):
        track = next(Track.search("SAINt JHN 5 Thousand Singles", limit=1))
        print(track)
        track = Track.from_url("https://open.spotify.com/track/0fFWxRZGKR7HDW2xBMOZgW")
        print(track)
        track.download("SAINt JHN - 5 Thousand Singles.mp3")
