#!/usr/bin/env bash
args="$@"
vagrant ssh -c "source ./venv/campenco/bin/activate && cd ./campenco/ && python ./app/manage.py $args"
