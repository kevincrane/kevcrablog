from flask import flash, request, redirect, url_for
import flask
from flask.ext.admin import BaseView, expose, AdminIndexView
from flask.ext.admin.contrib.fileadmin import FileAdmin
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.login import current_user, logout_user

from app.core import db
from app.kevcrablog.forms import PostForm
from app.kevcrablog.models import Post


class AdminMain(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated():
            login_url = '%s?next=%s' % (url_for('user.login'), flask.request.url)
            return redirect(login_url)
        else:
            return self.render('admin/index.html')

    @expose('/logout')
    def logout(self):
        logout_user()
        return redirect(url_for('blog.index'))


class NewPostView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated()

    @expose('/', methods=('GET', 'POST'))
    def new_post(self):
        """ Display the 'new post' live text editor form
        """
        # Validate the form and ensure this Post title doesn't already exist
        form = PostForm()
        if form.validate_on_submit() and not Post.query.filter_by(title=form.title.data).first():
            new_post = Post(title=form.title.data, body=form.body.data, author_id=1)
            db.session.add(new_post)
            db.session.commit()
            flash('Your post is now live!', 'success')
            return self.render('admin/index.html')
        elif request.method == 'POST':
            flash("There was a problem submitting the form (probably not a unique post title)!", 'danger')
        return self.render('admin/new_post.html', form=form)


class FileAdminView(FileAdmin):
    def is_accessible(self):
        return current_user.is_authenticated()


class PostAdminView(ModelView):
    """ Admin page for the management of blog posts
    """

    def is_accessible(self):
        return current_user.is_authenticated()

    def __init__(self):
        super(PostAdminView, self).__init__(Post, db.session)

    can_create = False  # Need to go to Markdown editor to create new pages.
    column_default_sort = ('created', True)