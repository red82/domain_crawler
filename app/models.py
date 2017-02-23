from app import db


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    domains = db.Column(db.String)

    def __repr__(self):
        return 'Request is: <<%s>>' % (self.id, )

