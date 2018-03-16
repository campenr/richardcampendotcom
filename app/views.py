# Copyright 2017 Richard Campen
# All rights reserved
# This software is released under the Modified BSD license
# See LICENSE.txt for the full license documentation

from flask import render_template
from app import flask_app
from app.models import Software


@flask_app.route('/')
@flask_app.route('/index')
def index():
    return render_template("index.html")


@flask_app.route('/software')
def software():

    software_versions = {software_.name: software_.version for software_ in Software.query.all()}

    return render_template('software.html', software_versions=software_versions)


@flask_app.route('/publications')
def publications():
    return render_template('publications.html')


@flask_app.route('/projects')
def projects():
    return render_template('projects.html')


@flask_app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
