# Copyright 2017 Richard Campen
# All rights reserved
# This software is released under the Modified BSD license
# See LICENSE.txt for the full license documentation

from flask import Flask
from celery import Celery
import os

from config import config

flask_app = Flask(__name__)

# load correct config settings based on environment variable
config_name = os.environ.get('CONFIG_ENV')
print('-Loading configuration: ', config_name)
flask_app.config.from_object(config[config_name])


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

celery_app = make_celery(flask_app)

from app import views
