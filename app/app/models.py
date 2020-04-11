from app import db


class Software(db.Model):

    __tablename__ = 'software'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    service = db.Column(db.String(64))
    version = db.Column(db.String(64))
