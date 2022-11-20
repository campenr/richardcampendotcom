#!/bin/sh

cd app
/app/venv/bin/python -m gunicorn wsgi:flask_app -b 0.0.0.0:4325
