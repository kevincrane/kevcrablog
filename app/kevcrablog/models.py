from datetime import datetime
from markdown.extensions.headerid import slugify
from sqlalchemy import desc
from app import db
from app.models import User


class Post(db.Model):
    """ Information about a full blog post
    """
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    author_id = db.Column(db.Integer, db.ForeignKey(User.id))
    # TODO: tags for each post?

    @classmethod
    def query_all(cls):
        return Post.query.order_by(desc(Post.created))

    @property
    def slug(self):
        return slugify(self.title, '-')

    def __repr__(self):
        return '<Post %s' % self.title
