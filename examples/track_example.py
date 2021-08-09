from dotify import Dotify, models

if __name__ == "__main__":
    with Dotify():
        track = next(models.Track.search("SAINt JHN 5 Thousand Singles", limit=1))

        print(track)

        track = models.Track.from_url("https://open.spotify.com/track/0fFWxRZGKR7HDW2xBMOZgW")

        print(track)

        track.download("SAINt JHN - 5 Thousand Singles.mp3")
