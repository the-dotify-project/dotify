![Dotify](/docs/img/logo.png)

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dotify)](https://www.python.org/)
[![PyPI](https://img.shields.io/pypi/v/dotify)](https://pypi.org/project/dotify/)
[![CI](https://github.com/billsioros/dotify/actions/workflows/ci.yml/badge.svg)](https://github.com/billsioros/dotify/actions/workflows/ci.yml)
[![docs](https://github.com/billsioros/dotify/actions/workflows/docs.yml/badge.svg)](https://billsioros.github.io/dotify/)
[![Maintainability](https://api.codeclimate.com/v1/badges/573685a448c6422d49de/maintainability)](https://codeclimate.com/github/billsioros/dotify/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/573685a448c6422d49de/test_coverage)](https://codeclimate.com/github/billsioros/dotify/test_coverage)
[![PyPI - License](https://img.shields.io/pypi/l/dotify)](/LICENSE)
[![GitHub commits since latest release (by SemVer)](https://img.shields.io/github/commits-since/billsioros/dotify/latest?style=flat-square)](https://github.com/billsioros/dotify/commits)

> _🚧 The project is currently under heavy development 🚧_

## Example Usage

```python
>>> from dotify import Dotify, Track
>>> with Dotify(SPOTIFY_ID, SPOTIFY_SECRET):
>>>     result = next(Track.search("SAINt JHN 5 Thousand Singles", limit=1))
>>> result
<Track "SAINt JHN - 5 Thousand Singles">
>>> result.url
'https://open.spotify.com/track/0fFWxRZGKR7HDW2xBMOZgW'
>>> result.download("SAINt JHN - 5 Thousand Singles.mp3")
PosixPath('SAINt JHN - 5 Thousand Singles.mp3')
```

Feel free to check the [examples](/examples) folder for more use case!

## Features

- Searching for
  - Tracks
  - Playlists
  - Albums
- Downloading
  - Tracks
  - Playlists
  - Albums

## Documentation

The project's documentation can be found [here](https://billsioros.github.io/dotify/).

## Installation

```bash
pip install dotify
```

## Contributing

If you would like to contribute to the project, please go through the [Contributing Guidelines](/CONTRIBUTING.md) first.

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://www.linkedin.com/in/vasileios-sioros/"><img src="https://avatars.githubusercontent.com/u/33862937?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Vasilis Sioros</b></sub></a><br /><a href="#maintenance-billsioros" title="Maintenance">🚧</a> <a href="#projectManagement-billsioros" title="Project Management">📆</a> <a href="https://github.com/billsioros/dotify/commits?author=billsioros" title="Documentation">📖</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
