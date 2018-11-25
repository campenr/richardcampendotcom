# Copyright 2017 Richard Campen
# All rights reserved
# This software is released under the Modified BSD license
# See LICENSE.txt for the full license documentation


from app import db
from sqlalchemy.dialects.postgresql.json import JSONB

class Software(db.Model):

    __tablename__ = 'software'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    # category = db.Column(db.String(64), nullable=False)
    # url = db.Column(db.String(256), nullable=False)
    service = db.Column(db.String(64))
    version = db.Column(db.String(64))
    # latest_url = db.Column(db.String(256))
    # other_urls = db.Column(JSONB)


