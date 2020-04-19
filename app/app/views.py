from flask import render_template
from config import flask_app


@flask_app.route('/')
def index():
    return render_template("index.html")


@flask_app.route('/software')
def software():
    return render_template('software.html')


@flask_app.route('/publications')
def publications():
    return render_template('publications.html')


@flask_app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
