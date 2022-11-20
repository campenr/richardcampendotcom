#!/usr/bin/env bash
args="$@"
./manage.sh "runserver --host=0.0.0.0 --port=4325 $args"
