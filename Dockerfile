FROM python:3.8-alpine

WORKDIR onesocial-reddit-oauth/

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY onesocial_reddit_oauth/ onesocial_reddit_oauth/

RUN ls

EXPOSE 8000

ENTRYPOINT ["uvicorn", "onesocial_reddit_oauth.app:app", "--host", "0.0.0.0"]