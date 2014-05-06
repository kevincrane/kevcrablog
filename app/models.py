from flask.ext.user import UserMixin
from app import db


class User(db.Model, UserMixin):
    """ Site-wide User model
    :param int id: unique user id
    :param str username: The name of the User
    :param str password: The User's password
    :param bool active: Is this user's account enabled?
    :param str email: The User's email
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, default='')
    active = db.Column(db.Boolean(), nullable=False, default=True)
    email = db.Column(db.String)

    def __init__(self, username, password, email='', active=True):
        self.username = username
        self.password = password
        self.email = email
        self.active = active