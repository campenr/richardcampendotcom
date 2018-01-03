# Copyright 2017 Richard Campen
# All rights reserved
# This software is released under the Modified BSD license
# See LICENSE.txt for the full license documentation

from app import celery_app, flask_app
from app.models import Software
import requests


@celery_app.task
def refresh_software_versions():

    softwares = Software.query.all()
    for software in softwares:

        tracker = flask_app.software_trackers[software.service](software.name)
        tracker.update_version()


@celery_app.task
def say_hello():

    print('Hello!')

    return 'hi'


@celery_app.task
def get_mothur_py():

    url_base = 'https://api.github.com'
    url = url_base + '/repos/campenr/mothur-py/releases/latest'

    r = requests.get(url)

    return r.json()