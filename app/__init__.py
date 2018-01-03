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

# celery setup
def make_celery(app):
    celery_ = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                     broker=app.config['CELERY_BROKER_URL'])
    celery_.conf.update(app.config)
    TaskBase = celery_.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery_.Task = ContextTask
    return celery_


print('-Configuring celery')
celery_app = make_celery(flask_app)


print('-Importing views, models, tasks, trackers')
from app import views, models, tasks, trackers

print('-Configuring trackers')
flask_app.software_trackers = {
    'pypi': trackers.PYPITracker
}

print('-Starting periodic background tasks')
refresh_versions = tasks.refresh_software_versions.apply_async(countdown=60)

