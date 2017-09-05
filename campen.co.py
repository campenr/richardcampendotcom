from flask import Flask, render_template
import requests
application = Flask(__name__)


@application.route('/')
@application.route('/index')
def index():
    return render_template("index.html")

@application.route('/publications')
def publications():
    return render_template('publications.html')

@application.route('/software')
def software():
    return render_template('software.html')

@application.route('/projects')
def projects():
    return render_template('projects.html')

@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    application.run()


# TODO: restructure website to use different pages for about, software, publications, etc.