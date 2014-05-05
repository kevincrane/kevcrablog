from flask import flash, request
from flask.ext.admin import BaseView, expose
from flask.ext.admin.contrib.sqla import ModelView
from app.core import db
from app.kevcrablog.forms import PostForm
from app.kevcrablog.models import Post


class AdminMain(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')


class NewPostView(BaseView):
    @expose('/', methods=('GET', 'POST'))
    def new_post(self):
        """ Display the 'new post' live text editor form
        """
        # Validate the form and ensure this Post title doesn't already exist
        form = PostForm()
        if form.validate_on_submit() and not Post.query.filter_by(title=form.title.data).first():
            new_post = Post(title=form.title.data, body=form.body.data, author_id=None)
            db.session.add(new_post)
            db.session.commit()
            flash('Your post is now live!', 'success')
            return self.render('admin/index.html')
        elif request.method == 'POST':
            flash("There was a problem submitting the form!", 'danger')
        return self.render('admin/new_post.html', form=form)


class PostAdminView(ModelView):
    """ Admin page for the management of blog posts
    """

    def __init__(self):
        super(PostAdminView, self).__init__(Post, db.session)

    can_create = False  # Need to go to Markdown editor to create new pages.
    column_default_sort = ('created', True)