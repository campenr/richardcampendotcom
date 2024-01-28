import os.path

from flask import Flask
from flask_sitemap import Sitemap

from whitenoise import WhiteNoise


flask_app = Flask(__name__)
flask_app.config.from_object('config')

sitemap = Sitemap(flask_app)

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))

flask_app.wsgi_app = WhiteNoise(
    flask_app.wsgi_app,
    root=os.path.join(ROOT_DIR, 'static'),
    prefix='static/',
)

from app import views, context_processors
