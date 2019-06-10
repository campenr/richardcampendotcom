import sys
import os

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app import flask_app, db

app = flask_app

# app.config.from_object('config')
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
