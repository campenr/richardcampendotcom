#!/usr/bin/env bash
args="$@"
./poetry.sh run "flask --debug run --host=0.0.0.0 --port=4325 $args"
