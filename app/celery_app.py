# Copyright 2018 Richard Campen
# All rights reserved
# This software is released under the Modified BSD license
# See LICENSE.txt for the full license documentation

"""
Define celery app here to avoid having to import entire application when
starting celery workers and celery beat.
"""

from celery import Celery
from app import flask_app


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
