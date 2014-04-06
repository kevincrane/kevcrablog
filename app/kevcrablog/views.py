from flask import Blueprint, render_template, flash, redirect, request, url_for
from app import db
from app.kevcrablog.forms import PostForm
from app.kevcrablog.models import Post
from settings import POSTS_PER_PAGE


blog = Blueprint('blog', __name__)


@blog.route('/')
@blog.route('/index', methods=['GET', 'POST'])
@blog.route('/index/<int:page>', methods=['GET', 'POST'])
# @cache.cached(timeout=1000)       # TODO add cache
def index(page=1):
    posts = Post.query_all().paginate(page, POSTS_PER_PAGE, False)  # TODO pagination
    return render_template('index.html',
                           posts=posts)


@blog.route('/newpost', methods=['GET', 'POST'])
def newpost():
    form = PostForm()

    # Validate the form and ensure this Post title doesn't already exist
    if form.validate_on_submit() and not Post.query.filter_by(title=form.title.data).first():
        post = Post(title=form.title.data, body=form.body.data, author_id=None)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!', 'success')
        return redirect(url_for('.index'))
    elif request.method == 'POST':
        flash("There was a problem submitting the form!", 'danger')
    return render_template('admin/new_post.html',
                           form=form)
