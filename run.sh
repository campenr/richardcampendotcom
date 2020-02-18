#!/usr/bin/env bash
args="$@"
vagrant ssh -c "tail -f -n0 ./logs/uwsgi/richardcampendotcom.log & sudo uwsgi --ini ./config/uwsgi/richardcampendotcom.ini $args"
