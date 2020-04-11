from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

from config import config

flask_app = Flask(__name__)

# load correct config settings based on environment variable, or default to 'development' environment
environment = os.environ.get('ENVIRONMENT')
if environment is None:
    print('-Loading configuration: No environment specified, defaulting to development environment')
    environment = 'development'
else:
    print('-Loading configuration: ', environment)
flask_app.config.from_object(config[environment])

# enable wekzeug debug traceback when running behind uWSGI
if environment == 'development':
    from werkzeug.debug import DebuggedApplication
    flask_app.wsgi_app = DebuggedApplication(flask_app.wsgi_app, True)

# db setup
db = SQLAlchemy(flask_app)

print('-Importing views, models')
from app import views, models

print('-Configuring trackers')
from app import trackers
flask_app.software_trackers = {
    'pypi': trackers.PYPITracker
}

print('-Init complete')
