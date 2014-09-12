from flask import Blueprint, render_template
from flask.ext.paginate import Pagination

from app import cache
from app.kevcrablog.models import Post
from settings import POSTS_PER_PAGE


blog = Blueprint('blog', __name__)


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
    return render_template('index.html', posts=posts, pagination=pagination,
                           recent_posts=recent, grouped_by_month=group_month)


@blog.route('/post/<int:post_id>-<slug>')
@cache.cached(timeout=3000)
def view_post(post_id, slug):
    """ Display a full new post, with comments and view count
    :param int post_id: id number of post to display
    :param str slug: slugified version of the post title
    """
    post = Post.query.get(post_id)
    if not post or post.slug != slug:
        return page_not_found(404)
    recent, group_month = sidebar()
    return render_template('post.html', post=post,
                           recent_posts=recent, grouped_by_month=group_month)


@blog.route('/about')
@cache.cached(timeout=6000)
def about():
    """ Display the About Me page
    """
    recent, group_month = sidebar()
    return render_template('about.html', recent_posts=recent, grouped_by_month=group_month)


@blog.errorhandler(404)
def page_not_found(e):
    """ Error Code 404 Handler
    """
    return render_template('error/404.html'), 404