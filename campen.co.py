from flask import Flask, render_template
import requests
application = Flask(__name__)


@application.route('/')
@application.route('/index')
@application.route('/publications')
@application.route('/software')
def index():

    return render_template("index.html")

@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    application.run()


# TODO: restructure website to use different pages for about, software, publications, etc.