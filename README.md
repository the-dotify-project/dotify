# Dotify

[![Build](https://github.com/billsioros/dotify/actions/workflows/build.yml/badge.svg)](https://github.com/billsioros/dotify/actions/workflows/build.yml)

- [Dotify](#dotify)
  - [Installation](#installation)
    - [System Dependencies](#system-dependencies)
    - [Virtual Environment](#virtual-environment)
    - [Pip Dependencies](#pip-dependencies)
  - [Development](#development)
    - [Running](#running)
  - [TODOs](#todos)

## Installation

### System Dependencies

```bash
sudo apt-get install python3
sudo apt-get install python3-pip
sudo apt-get install ffmpeg
```

### Virtual Environment

```bash
pip3 install virutalenv
virtualenv .env
. .env/bin/activate
```

### Pip Dependencies

```bash
pip install -r requirements
```

## Development

### Running

```bash
export FLASK_APP=backend/api.py
export FLASK_ENV=development
.env/bin/flask run
```

## TODOs

- [X] Exceptions
- [ ] SpotifyException
