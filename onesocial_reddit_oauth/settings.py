"""
This module uses to defined constant settings to Reddit OAuth.
- SCOPE: scopes are used by Onesocial app.
- DURATION: lifetime of access token.
- REDDIT_AUTHORIZE_URL: url to build oauth url.
- REDDIT_ACCESS_TOKEN_URL: url to get access token.
"""

SCOPE = (
    "identity edit flair history modconfig modflair modlog modposts modwiki mysubreddits "
    "privatemessages read report save submit subscribe vote wikiedit wikiread"
)
DURATION = "permanent"

REDDIT_AUTHORIZE_URL = "https://www.reddit.com/api/v1/authorize.compact"
REDDIT_ACCESS_TOKEN_URL = "https://www.reddit.com/api/v1/access_token"
