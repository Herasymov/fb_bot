from app import db

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    fb_id = db.Column(db.String(64), index=True, unique=True)
    fio = db.Column(db.String(128), index=True)
    phone = db.Column(db.Integer, index=True)
    status = db.Column(db.Integer, index=True)

    def __repr__(self):
        return "<User: {}, {}, {}, {}, {}>".format(self.user_id, self.fb_id, self.fio, self.phone, self.status)
