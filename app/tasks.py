# Copyright 2017 Richard Campen
# All rights reserved
# This software is released under the Modified BSD license
# See LICENSE.txt for the full license documentation

from celery import Celery

from app import celery_app, flask_app
from app.models import Software


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):

    # fire off tasks that should run each time the app starts
    refresh_software_versions.apply_async(countdown=60)

    # queue up tasks that should be run periodically
    sender.add_periodic_task(60*60*24, refresh_software_versions)


@celery_app.task
def refresh_software_versions():

    softwares = Software.query.all()
    for software in softwares:

        tracker = flask_app.software_trackers[software.service](software.name)
        tracker.update_version()
