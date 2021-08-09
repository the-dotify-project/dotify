![Dotify](https://raw.githubusercontent.com/the-dotify-project/dotify/master/docs/img/logo.png)

<p align="center">
  <a href="https://www.python.org/">
    <img
      src="https://img.shields.io/pypi/pyversions/dotify"
      alt="PyPI - Python Version"
    />
  </a>
  <a href="https://pypi.org/project/dotify/">
    <img
      src="https://img.shields.io/pypi/v/dotify"
      alt="PyPI"
    />
  </a>
  <a href="https://github.com/the-dotify-project/dotify/actions/workflows/ci.yml">
    <img
      src="https://github.com/the-dotify-project/dotify/actions/workflows/ci.yml/badge.svg"
      alt="CI"
    />
  </a>
  <a href="https://github.com/the-dotify-project/dotify/actions/workflows/cd.yml">
    <img
      src="https://github.com/the-dotify-project/dotify/actions/workflows/cd.yml/badge.svg"
      alt="CI"
    />
  </a>
  <a href="https://results.pre-commit.ci/latest/github/the-dotify-project/dotify/master">
    <img
      src="https://results.pre-commit.ci/badge/github/the-dotify-project/dotify/master.svg"
      alt="pre-commit.ci status"
    />
  </a>
  <a href="https://codecov.io/gh/the-dotify-project/dotify">
    <img
      src="https://codecov.io/gh/the-dotify-project/dotify/branch/master/graph/badge.svg?token=coLOL0j6Ap"
      alt="Test Coverage"/>
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img
      src="https://img.shields.io/pypi/l/dotify"
      alt="PyPI - License"
    />
  </a>
  <a href="https://gitpod.io/from-referrer/">
    <img
      src="https://img.shields.io/badge/Gitpod-Open-blue?logo=gitpod"
      alt="Open on Gitpod"
    />
  </a>
</p>

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

Feel free to check the [examples](https://github.com/the-dotify-project/dotify/tree/master/examples) folder for more use cases!

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

The project's documentation can be found [here](https://the-dotify-project.github.io/dotify/).

## Installation

```bash
pip install dotify
```

## Supporting the project

Feel free to [**Buy me a coffee! ☕**](https://www.buymeacoffee.com/billsioros).

## Contributing

If you would like to contribute to the project, please go through the [Contributing Guidelines](https://the-dotify-project.github.io/dotify/latest/CONTRIBUTING/) first.

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
