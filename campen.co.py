from flask import Flask, render_template
application = Flask(__name__)

@application.route("/")
@application.route("/index")
def homepage():
    return render_template("index.html")

@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    application.run()