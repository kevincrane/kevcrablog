from flask import Blueprint, render_template
from app import cache
from app.kevcrablog.models import Post

base = Blueprint('base', __name__)


@base.route('/')
def index():
    """ Main site index page
    """
    # TODO HERE:
    #     - Show hero image of something
    #     - footer
    frontpage_posts = Post.query_all().slice(0, 4)
    return render_template('index.html', frontpage_posts=frontpage_posts)


@base.route('/about')
@cache.cached(timeout=600)
def about():
    """ Display the About Me page
    """
    return render_template('about.html')


@base.errorhandler(404)
def page_not_found(e):
    """ Error Code 404 Handler
    """
    return render_template('error/404.html'), 404


@base.errorhandler(Exception)
def unhandled_exception(e):
    # TODO: real error page
    return render_template('error/404.html'), 404