from flask import Flask, render_template
application = Flask(__name__)

@application.route("/")
@application.route("/index")
def homepage():
    return render_template("index.html")

if __name__ == "__main__":
    application.run()