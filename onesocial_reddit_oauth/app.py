"""
This module is Onesocial Reddit OAuth service. It provides 2 urls:
- /create-url: generate url to authorize to Reddit.
- /access-token: get access token after user login to Reddit.
"""

import os
import random
import string
from base64 import b64encode
from typing import Callable, Union
from urllib.parse import urlencode

import httpx
from fastapi import Depends, FastAPI, Request, Response
from starlette.middleware.sessions import SessionMiddleware
from typing_extensions import Annotated

from onesocial_reddit_oauth import settings

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=os.getenv("CLIENT_SECRET"))


def _create_state():
    return "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(16)
    )


def _get_authorization():
    return b64encode(
        f'{os.getenv("CLIENT_ID")}:{os.getenv("CLIENT_SECRET")}'.encode()
    ).decode()


def _get_access_token():
    def inner(code: Union[str, None]):
        if code is None:
            return None
        headers = {
            "User-Agent": "Onesocial Reddit OAuth Service",
            "Authorization": f"Basic {_get_authorization()}",
        }
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": os.getenv("REDIRECT_URI"),
        }
        res = httpx.post(
            settings.REDDIT_ACCESS_TOKEN_URL, data=payload, headers=headers
        )
        if res.status_code != 200:
            return None
        return res.json()

    return inner


@app.get("/create-url")
def create_url(req: Request):
    """
    /create-url: generate url to authorize to Reddit.
    :return:
        - url: Built url used to oauth Reddit.
    """
    state = _create_state()
    params = {
        "client_id": os.getenv("CLIENT_ID"),
        "response_type": "code",
        "state": state,
        "redirect_uri": os.getenv("REDIRECT_URI"),
        "duration": settings.DURATION,
        "scope": settings.SCOPE,
    }
    req.session[f"state-{state}"] = params
    return {"url": f"{settings.REDDIT_AUTHORIZE_URL}?{urlencode(params)}"}


@app.get("/access-token")
def get_access_token(
    req: Request,
    state: str,
    _get_access_token: Annotated[Callable, Depends(_get_access_token)],
    error: Union[str, None] = None,
    code: Union[str, None] = None,
):
    """
    /access-token: get access token after user login to Reddit.
    :params:
        - error: error state when user login to Reddit
        - state: state value generated in /create-url
        - code: returned code from Reddit
    :return:
        - token: token info that returned from Reddit
    """
    if error:
        return Response(f"reddit {error}", status_code=400)
    if f"state-{state}" not in req.session:
        return Response("state not match", status_code=400)
    del req.session[f"state-{state}"]
    data = _get_access_token(code)
    if data is None:
        return Response("code invalid", status_code=400)
    return {"token": data}
