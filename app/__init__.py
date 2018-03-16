# Copyright 2017 Richard Campen
# All rights reserved
# This software is released under the Modified BSD license
# See LICENSE.txt for the full license documentation

from flask import Flask
from celery import Celery
from flask_sqlalchemy import SQLAlchemy
import os

from config import config

flask_app = Flask(__name__)

# load correct config settings based on environment variable, or default to 'development' environment
config_name = os.environ.get('CONFIG_ENV')
if config_name is None:
    print('-Loading configuration: No environment specified, defaulting to development environment')
    config_name = 'development'
else:
    print('-Loading configuration: ', config_name)
flask_app.config.from_object(config[config_name])

# db setup
db = SQLAlchemy(flask_app)

print('-Importing views and models')
from app import views, models

print('-Configuring trackers')
from app import trackers
flask_app.software_trackers = {
    'pypi': trackers.PYPITracker
}

print('-Configuring tasks and queuing periodic tasks')
from app.celery_app import celery_app
from app import tasks
