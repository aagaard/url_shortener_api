# URL shortener API

A simple REST API to shorten a URL using [FastAPI](https://fastapi.tiangolo.com/) ⚡️.

## Getting Started

### Prerequisites

It is assumed the following packages are installed before using [HomeBrew](https://brew.sh/) on macOS:
``` shell
brew install curl python@3.9
```

With Python3.9 in the `PATH`, run the following to install [Poetry](https://python-poetry.org/) (a package and dependency manager):
``` shell
curl -sSL https://install.python-poetry.org | python -
```

### Prepare and install the environment

Clone the project:
``` shell
git clone https://github.com/aagaard/url_shortener_api
```

To configure poetry to install the virtual environment in the project and install the project inside the virtual environment
``` shell
poetry config settings.virtualenvs.in-project true
poetry install
```

## Start the server

Run the web application in "production" mode (be aware the server is publicly available):

``` shell
poetry run app/main.py
```

To run the web application in developer mode (reloads application for every file change):

``` shell
poetry run uvicorn app.main:app --reload
```

## To run tests

``` shell
poetry run pytest
```

