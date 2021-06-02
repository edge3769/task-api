from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tags = db.Column(db.JSON)
    username = db.Column(db.Unicode)
    location = db.Column(db.JSON)
    distance = db.Column(db.Float)
    visible = db.Column(db.Boolean, default=True)
    score = db.Column(db.Integer)

    def __init__(self, username, id):
        self.id = id
        self.username = username
        db.session.add(self)
        db.session.commit()

    def dict(self):
        return {
            'id': self.id,
            'tags': self.tags,
            'username': self.username,
            'location': self.location,
            'visible': self.visible,
        }