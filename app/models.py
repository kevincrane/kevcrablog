from app import db


class User(db.Model):
    """ Site-wide User model
    """
    # TODO: actually use this right; Flask-Login or Flask-Security; add @login-required tags, admin roles
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String)

    def __init__(self, username, password):
        self.username = username
        self.password = password