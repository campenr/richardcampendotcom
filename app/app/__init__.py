from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_sitemap import Sitemap


flask_app = Flask(__name__)
flask_app.config.from_object('config')

# enable werkzeug debug traceback when running behind uWSGI
if flask_app.config.get('DEBUG') is True:
    from werkzeug.debug import DebuggedApplication
    flask_app.wsgi_app = DebuggedApplication(flask_app.wsgi_app, True)

db = SQLAlchemy(flask_app)
sitemap = Sitemap(flask_app)

from app import views, models
