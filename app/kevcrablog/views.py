from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask.ext.paginate import Pagination
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
    """ Display the main page of the blog with the most recent blog posts
        paginated and displayed
    """
    posts = Post.query_all().paginate(page, POSTS_PER_PAGE, False)  # TODO pagination
    pagination = Pagination(page=page, total=posts.total, per_page=POSTS_PER_PAGE, record_name='posts', bs_version=3)
    return render_template('index.html',
                           posts=posts, pagination=pagination)


@blog.route('/post/<int:post_id>/<slug>')
def view_post(post_id, slug):
    """ Display a full new post, with comments and view count
    """
    post = Post.query.get(post_id)
    if not post:
        return page_not_found(404)
    prev_page = request.args.get('prev_page', None)
    return render_template('post.html', post=post, prev_page=prev_page)


@blog.route('/newpost', methods=['GET', 'POST'])
def newpost():
    """ Display the 'new post' live text editor form
    """
    # Validate the form and ensure this Post title doesn't already exist
    form = PostForm()
    if form.validate_on_submit() and not Post.query.filter_by(title=form.title.data).first():
        new_post = Post(title=form.title.data, body=form.body.data, author_id=None)
        db.session.add(new_post)
        db.session.commit()
        flash('Your post is now live!', 'success')
        return redirect(url_for('.index'))
    elif request.method == 'POST':
        flash("There was a problem submitting the form!", 'danger')
    return render_template('admin/new_post.html',
                           form=form)


@blog.errorhandler(404)
def page_not_found(e):
    """ Error Code 404 Handler
    """
    return render_template('error/404.html'), 404