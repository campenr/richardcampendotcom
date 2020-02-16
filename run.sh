#!/usr/bin/env bash
args="$@"
vagrant ssh -c "sudo uwsgi --ini ./config/uwsgi/richardcampendotcom.uwsgi.ini $args"
