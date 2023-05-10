# Onesocial Reddit OAuth

OAuth service for Reddit.

## Requirements

```
Python 3.8.10
Poetry 1.4.2
Docker 23.0.5
```

## Setup

Copy `.env.example` to `.env` and update enviroment variables.

```
poetry install
```

## Run

Run local:

```
sh ./serve.sh
```

Run with Docker:

```
docker build -t onesocial-reddit-oauth .
docker run -d -p 8000:8000 --file-env .env onesocial-reddit-oauth
```

## Test

```
sh ./test.sh
```
