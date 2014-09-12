import calendar
import collections
from datetime import datetime
from itertools import groupby

from markdown.extensions.headerid import slugify
from sqlalchemy import desc

from app import db
from app.models import User


class Post(db.Model):
    """ A Post defining a blog article
    :param int id: Unique id for this post
    :param str title: Unique blog post title
    :param str body: The complete text of the post, written in Markdown
    :param datetime created: When the post was created
    :param int author_id: the id of the author who wrote this article (possibly worthless)
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
        """ Return all stored, ordered in reverse chronological (newest to oldest)
        :return Query:
        """
        return Post.query.order_by(desc(Post.created))

    @classmethod
    def group_by_year_month(cls):
        """ Returns all posts grouped by year and month
        :return dict: { (year, month): [Posts] }
        """
        order_group = collections.OrderedDict()
        posts = Post.query.with_entities(Post.id, Post.title, Post.created).order_by(desc(Post.created))
        for ((year, month), grouped_posts) in groupby(posts, lambda x: (x.created.year, x.created.month)):
            grouped = []
            for post in grouped_posts:
                slugged_post = post._asdict()
                slugged_post['slug'] = slugify(post.title, '-')
                grouped.append(slugged_post)

            order_group[(year, calendar.month_name[month])] = grouped
        return order_group

    @property
    def slug(self):
        """ Returns 'sluggified' version of the title
        :return str:
        """
        return slugify(self.title, '-')

    def __repr__(self):
        return '<Post %s>' % self.title
