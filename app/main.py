#!/usr/bin/env python
import random
from string import ascii_letters, digits
from typing import Optional, Union

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from pydantic.networks import HttpUrl
from pydantic.tools import parse_obj_as

from .bdict import BiDict

PROJECT_NAME = "url_shortener"
DEBUG = True
VERSION = "v1"

VALID_URL_CHARACTERS = ascii_letters + digits
SHORTEN_URL_LENGTH = 6

app = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)
db = BiDict()

class ShortenUrlNotFoundError(Exception):
    ...

class UrlShortenerRequest(BaseModel):
    url: HttpUrl


class UrlShortenerResponse(BaseModel):
    url: HttpUrl
    short: Union[HttpUrl, str]

def generate_shorten_url(*, base_url: Optional[HttpUrl] = None) -> Union[HttpUrl, str]:
    "Generate shorten url either relative to host url or with `base_url`."
    unqiue_rel_url = "".join(random.sample(VALID_URL_CHARACTERS, SHORTEN_URL_LENGTH))
    if base_url:
        shorten_url = base_url.join(unqiue_rel_url)
        return parse_obj_as(HttpUrl, shorten_url)
    return unqiue_rel_url


def store(url: str, shorten_url: str) -> None:
    """Store `url` with reference to `shorten_url`."""
    db[shorten_url] = url


def retrieve_original_url(shorten_url: str) -> str:
    """Fetch the original URL using the `shorten_url`"""
    try:
        return db[shorten_url]
    except KeyError as e:
        raise ShortenUrlNotFoundError(e)


@app.post("/urls", status_code=201)
async def urls(url: UrlShortenerRequest):
    """Shorten `url`."""
    url_short = generate_shorten_url()
    store(url=str(url.url), shorten_url=url_short)
    return UrlShortenerResponse(url=url.url, short="/" + url_short)


@app.get("/{shorten_url}")
async def convert_url(shorten_url: str):
    """Convert `shorten_url` to its original url."""
    try:
        original_url = retrieve_original_url(shorten_url)
    except ShortenUrlNotFoundError:
        raise HTTPException(detail="Shorten URL is not found", status_code=404)

    return RedirectResponse(url=original_url, status_code=301)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=False, debug=False)
