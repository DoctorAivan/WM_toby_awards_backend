#!/bin/sh

docker build -t gala-cracks-backend -f docker/Dockerfile .
docker-compose -f docker/docker-compose.yml up -d