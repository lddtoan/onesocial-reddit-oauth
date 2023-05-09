import re
from fastapi.testclient import TestClient
from onesocial_reddit_oauth.app import app


client = TestClient(app)


def test_create_url():
    res = client.get("/create-url")
    assert res.status_code == 200
    assert re.match(
        r"^https:\/\/www.reddit.com\/api\/v1\/authorize.compact\?client_id=test&response_type=code&state=[\w]{16}&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fcallback&duration=permanent&scope=identity\+edit\+flair\+history\+modconfig\+modflair\+modlog\+modposts\+modwiki\+mysubreddits\+privatemessages\+read\+report\+save\+submit\+subscribe\+vote\+wikiedit\+wikiread$",
        res.json()["url"],
    )


def test_get_access_token():
    pass
