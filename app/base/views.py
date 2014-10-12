from flask import Blueprint, render_template, send_from_directory, request
from app import cache
from app.kevcrablog.models import Post

base = Blueprint('base', __name__)


@base.route('/')
def index():
    """ Main site index page
    """
    frontpage_posts = Post.query_all().slice(0, 3)
    return render_template('index.html', frontpage_posts=frontpage_posts)


@base.route('/about')
@cache.cached(timeout=600)
def about():
    """ Display the About Me page
    """
    return render_template('about.html', title='About')


@base.route('/projects')
@cache.cached(timeout=600)
def projects():
    """ Display the Projects page
    """
    return render_template('projects.html', title='Projects')



# Error Handlers and Miscellaneous
@base.app_errorhandler(404)
def page_not_found(e):
    """ Error Code 404 Handler
    """
    return render_template('error/404.html'), 404

@base.app_errorhandler(404)
def server_error(e):
    """ Error Code 404 Handler
    """
    return render_template('error/500.html'), 500


@base.app_errorhandler(Exception)
def unhandled_exception(e):
    # TODO: real error page
    return render_template('error/500.html', error=e), 500
