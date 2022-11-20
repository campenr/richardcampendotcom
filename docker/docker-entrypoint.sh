#!/bin/sh

cd app
python -m gunicorn app.asgi:application -b 0.0.0.0:8080 -k uvicorn.workers.UvicornWorker
