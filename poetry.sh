#!/usr/bin/env bash
args="$@"
docker-compose -f docker/docker-compose.dev.yml exec flask sh -c ". /venv/bin/activate && cd app/ && LANG=C.UTF-8 poetry $args"
