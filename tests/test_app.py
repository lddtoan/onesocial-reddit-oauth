"""
Module tests Onesocial Reddit OAuth services. It has 2 tests:
- test_create_url: test /create-url
- test_get_access_token: test /access-token
"""

import re
from typing import Union

from fastapi.testclient import TestClient

from onesocial_reddit_oauth.app import _get_access_token, app

client = TestClient(app)


def test_create_url():
    """
    Assert 2 values:
    - status_code == 200
    - url match regex
    """
    res = client.get("/create-url")
    url = res.json()["url"]

    assert res.status_code == 200
    assert re.match(
        r"^https:\/\/www.reddit.com\/api\/v1\/authorize.compact\?client_id=test&"
        r"response_type=code&state=[\w]{16}&redirect_uri=http%3A%2F%2Flocalhost"
        r"%3A3000%2Fcallback&duration=permanent&scope=identity\+edit\+flair\+history"
        r"\+modconfig\+modflair\+modlog\+modposts\+modwiki\+mysubreddits\+privatemessages"
        r"\+read\+report\+save\+submit\+subscribe\+vote\+wikiedit\+wikiread$",
        url,
    )


def _override_get_access_token():
    def inner(code: Union[str, None]):
        if code != "test":
            return None
        return {
            "access_token": "test",
            "token_type": "bearer",
            "expires_in": 86400,
            "refresh_token": "test",
            "scope": "wikiedit save wikiread modwiki edit vote mysubreddits subscribe "
            "privatemessages modconfig read modlog modposts modflair report flair "
            "submit identity history",
        }

    return inner


app.dependency_overrides[_get_access_token] = _override_get_access_token


def test_get_access_token():
    """
    Assert 2 values:
    - status_code == 200
    - compare response token
    """
    res = client.get("/create-url")
    url = res.json()["url"]
    _state = re.search(r"state=([\w]{16})", url).group(1)

    res = client.get(f"/access-token?code=test&state={_state}")
    assert res.status_code == 200
    assert res.json() == {
        "token": {
            "access_token": "test",
            "token_type": "bearer",
            "expires_in": 86400,
            "refresh_token": "test",
            "scope": "wikiedit save wikiread modwiki edit vote mysubreddits subscribe "
            "privatemessages modconfig read modlog modposts modflair report flair "
            "submit identity history",
        }
    }
