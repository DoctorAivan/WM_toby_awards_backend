#!/bin/sh

gunicorn -w 8 \
          -k gevent \
          --worker-connections 1000 \
          --access-logfile logs/access_log \
          --error-logfile logs/error_log \
          --bind :80 \
          core.wsgi:application
