#!/bin/sh
args="$@"
docker-compose -f ./docker/docker-compose.dev.yml up $args
