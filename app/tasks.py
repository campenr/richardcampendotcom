# Copyright 2017 Richard Campen
# All rights reserved
# This software is released under the Modified BSD license
# See LICENSE.txt for the full license documentation

from app import celery_app, flask_app
from app.models import Software


@celery_app.task
def refresh_software_versions():

    softwares = Software.query.all()
    for software in softwares:

        tracker = flask_app.software_trackers[software.service](software.name)
        tracker.update_version()
