# Copyright 2017 Richard Campen
# All rights reserved
# This software is released under the Modified BSD license
# See LICENSE.txt for the full license documentation

from app import flask_app

if __name__ == '__main__':
    # flask_app.run(debug=True, host='0.0.0.0', port=5000)
    flask_app.run(debug=True, host='0.0.0.0')
