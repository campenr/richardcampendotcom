# Copyright 2017 Richard Campen
# All rights reserved
# This software is released under the Modified BSD license
# See LICENSE.txt for the full license documentation

from flask import Flask
from celery import Celery
import os

from config import config

flask_app = Flask(__name__)

# load correct config settings based on environment variable, or default to 'development' environment
config_name = os.environ.get('CONFIG_ENV')
if config_name is None:
    print('-Loading configuration: No environment specififed, defaulting to development environment')
    config_name = 'development'
else:
    print('-Loading configuration: ', config_name)
flask_app.config.from_object(config[config_name])

# celery setup
celery_app = Celery(flask_app.name)
celery_app.conf.update(flask_app.config)

from app import views
