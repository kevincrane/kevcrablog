from flask.ext.admin import BaseView, expose
from flask.ext.admin.contrib.sqla import ModelView
from app.core import db
from app.kevcrablog.models import Post


class AdminMain(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')


class PostAdminView(ModelView):
    """ Admin page for the management of blog posts
    """

    def __init__(self):
        super(PostAdminView, self).__init__(Post, db.session)

    can_create = False  # Need to go to Markdown editor to create new pages.
    column_default_sort = ('created', True)