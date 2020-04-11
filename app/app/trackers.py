from app import db
from app.models import Software
import requests


class SoftwareTracker(object):

    def __init__(self, name):

        self.name = name
        self.url = ''

    def parse_version(self):
        """Method for parsing version number. Must implement in Subclass."""

        pass

    def update_version(self):

        try:
            # get version using Tracker specific parser
            version = self.parse_version()

            # update database record
            software = Software.query.filter_by(name=self.name).first()
            software.version = version
            db.session.commit()

        except Exception as e:
            print('Got the following exception when fetching version number for {name}:\n'
                  '[START]{e}[END]'.format(name=self.name, e=e))


class PYPITracker(SoftwareTracker):

    def __init__(self, name):
        super().__init__(name)
        self.url = 'https://pypi.python.org/pypi/{name}/json'.format(name=self.name)

    def parse_version(self):
        """Parse software version from PYPI."""

        r = requests.get(url=self.url)
        version = r.json()['info']['version']

        return version
