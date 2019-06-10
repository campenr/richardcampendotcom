#!/usr/bin/env bash
vagrant ssh -c "source ./venv/campenco/bin/activate && cd ./campenco/ && python -m pip install -r ./app/requirements.txt"
