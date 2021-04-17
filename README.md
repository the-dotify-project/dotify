# Dotify

> **Because OOP is the light**

[![Test](https://github.com/billsioros/dotify/actions/workflows/test.yml/badge.svg)](https://github.com/billsioros/dotify/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/billsioros/dotify/branch/master/graph/badge.svg?token=3F4OYLDW7P)](https://codecov.io/gh/billsioros/dotify)
![PyPI](https://img.shields.io/pypi/v/dotify)

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

## Installation

```bash
pip install dotify
```

*Will be publishing to PyPI soon !*

## License

<img align="right" src="http://opensource.org/trademarks/opensource/OSI-Approved-License-100x137.png">

The project is licensed under the [MIT License](http://opensource.org/licenses/MIT):

Copyright &copy; 2020 [Vasileios Sioros](https://github.com/billsioros)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
