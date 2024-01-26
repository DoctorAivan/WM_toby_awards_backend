FROM python:3.9-alpine

ENV PRODUCTION=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt && pip install gunicorn gevent

# Run django app with gunicorn
ENTRYPOINT ./docker/entrypoint.sh
