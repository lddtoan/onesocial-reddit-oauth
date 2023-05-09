export $(xargs < .env)
uvicorn onesocial_reddit_oauth.app:app --reload