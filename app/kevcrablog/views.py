from flask import Blueprint, flash, redirect, render_template, url_for, request
from flask.ext.paginate import Pagination

from app import cache
from app.base.views import page_not_found
from app.core import db
from app.kevcrablog.forms import CommentForm
from app.kevcrablog.models import Post, Comment
from settings import POSTS_PER_PAGE


blog = Blueprint('blog', __name__, url_prefix='/blog')


def sidebar():
    """ Fetch a dict of information that should be used for each view
        e.g. recent posts, posts by view used in base_blog.html
    """
    recent_posts = Post.query_all().limit(5)
    grouped_by_month = Post.group_by_year_month()
    return recent_posts, grouped_by_month


@blog.route('/')
@blog.route('/index/', methods=['GET', 'POST'])
@blog.route('/index/<int:page>', methods=['GET', 'POST'])
@cache.cached(timeout=3000)
def index(page=1):
    """ Display the main page of the blog with the most recent blog posts
        paginated and displayed
    :param int page: Which paginated page of blog entries to display
    """
    posts = Post.query_all().paginate(page, POSTS_PER_PAGE, False)
    pagination = Pagination(page=page, total=posts.total, per_page=POSTS_PER_PAGE,
                            record_name='posts', bs_version=3)
    recent, group_month = sidebar()
    return render_template('kevcrablog/index.html', posts=posts, pagination=pagination,
                           recent_posts=recent, grouped_by_month=group_month)


@blog.route('/post/<int:post_id>-<slug>', methods=['GET', 'POST'])
# @cache.cached(timeout=300)
def view_post(post_id, slug):
    """ Display a full new post, with comments and view count
    :param int post_id: id number of post to display
    :param str slug: slugified version of the post title
    """
    post = Post.query.get(post_id)
    form = CommentForm()
    if not post or post.slug != slug:
        return page_not_found(404)

    if request.method == 'POST' and form.validate_on_submit():
        # Handle new comment, redirect to same post
        new_comment = Comment(body=form.body.data, author=form.author.data)
        post.comments.append(new_comment)
        db.session.commit()
        flash('Your comment is now live!', 'success')
        return redirect(url_for('.view_post', post_id=post_id, slug=slug))

    recent, group_month = sidebar()
    return render_template('kevcrablog/post.html', post=post,
                           recent_posts=recent, grouped_by_month=group_month, form=form)
