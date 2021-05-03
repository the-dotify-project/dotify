# Dotify

> **Because OOP is the light**

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dotify)](https://www.python.org/)
[![PyPI](https://img.shields.io/pypi/v/dotify)](https://pypi.org/project/dotify/)
[![CI](https://github.com/billsioros/dotify/actions/workflows/ci.yml/badge.svg)](https://github.com/billsioros/dotify/actions/workflows/ci.yml)
[![docs](https://github.com/billsioros/dotify/actions/workflows/docs.yml/badge.svg)](https://billsioros.github.io/dotify/)
[![Maintainability](https://api.codeclimate.com/v1/badges/573685a448c6422d49de/maintainability)](https://codeclimate.com/github/billsioros/dotify/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/573685a448c6422d49de/test_coverage)](https://codeclimate.com/github/billsioros/dotify/test_coverage)
[![PyPI - License](https://img.shields.io/pypi/l/dotify)](/LICENSE)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

*🚧 The project is under development 🚧*

## Example

```python
>>> from dotify import Dotify, Track
>>> with Dotify(SPOTIFY_CLIENT, SPOTIFY_SECRET):
>>>     result = next(Track.search("SAINt JHN 5 Thousand Singles", limit=1))
>>> result
<Track "SAINt JHN - 5 Thousand Singles">
>>> result.url
'https://open.spotify.com/track/0fFWxRZGKR7HDW2xBMOZgW'
>>> result.download("SAINt JHN - 5 Thousand Singles.mp3")
PosixPath('SAINt JHN - 5 Thousand Singles.mp3')
```

## Documentation

The project's documentation can be found [here](https://billsioros.github.io/dotify/).

## Installation

```bash
pip install dotify
```

## Contributing

If you would like to contribute to the project, please go through the [Contributing Guidelines](/CONTRIBUTING.md) first.
