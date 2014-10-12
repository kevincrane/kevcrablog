# !/usr/bin/env python
import os

from flask import Flask, url_for
from flask.ext.admin import Admin
from flask.ext.babel import Babel
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.misaka import Misaka
from flask.ext.moment import Moment
from flask.ext.user import UserManager, SQLAlchemyAdapter
from flask.ext.cache import Cache  # TODO add caching
from flask.ext.assets import Bundle, Environment
from app.base.admin import AdminMain, PostAdminView, NewPostView, FileAdminView
from app.core import db  # TODO: can you just move the one line from core.py to here (or below imports?)

cache = Cache(config={'CACHE_TYPE': 'simple'})
from app.base import views as views_base
from app.kevcrablog import views as views_blog

from app.kevcrablog.models import Post
from app.base.models import User
from settings import BASE_DIR


def create_app(config='dev'):
    """ Flask application factory
    :param str config: type of app to build, either "prod" or "dev"
    """
    # Create flask application
    app = Flask(__name__)
    app.config.from_object('settings')
    app.config['ENV'] = config
    app.jinja_env.trim_blocks = True

    # Debug toolbar (when debug=true)
    debug_toolbar = DebugToolbarExtension(app)
    app.config['DEBUG_TB_PROFILER_ENABLED'] = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    # Register Blueprints
    app.register_blueprint(views_base.base)
    app.register_blueprint(views_blog.blog)

    # Flask-Assets; bundles all css/js files in minifed file
    assets = Environment(app)
    css_all = Bundle('css/bootstrap-flatly.min.css', 'css/highlightjs.min.css', 'css/font-awesome.css', 'css/main.css',
                     filters='cssmin', output='gen/style.css')
    js_all = Bundle('js/vendor/bootstrap.min.js', 'js/vendor/showdown-gfm.min.js', 'js/vendor/highlight.min.js',
                    'js/vendor/moment.min.js', 'js/main.js', filters='jsmin', output='gen/libs.js')
    assets.register('css_all', css_all)
    assets.register('js_all', js_all)
    if app.config['DEBUG']:
        assets.debug = True
        app.config['ASSETS_DEBUG'] = True

    # Set up Flask-User
    babel = Babel(app)
    db_adapter = SQLAlchemyAdapter(db, User)
    user_manager = UserManager(db_adapter, app)  # Init Flask-User and bind to app

    # Init the cache
    cache.init_app(app)

    Moment(app)  # moment.js
    Misaka(app, autolink=True,  # Misaka Markdown
           fenced_code=True, lax_html=True, strikethrough=True,
           superscript=True, tables=True, wrap=True)

    # Init Admin page
    admin = Admin(app, index_view=AdminMain(endpoint='admin'))
    admin.add_view(PostAdminView())
    admin.add_view(NewPostView())
    static_path = os.path.join(BASE_DIR, 'app', 'static')
    admin.add_view(FileAdminView(static_path, '/static/', name='Static Files'))

    # Initialize DB
    db.init_app(app)

    return app


if __name__ == '__main__':
    app = create_app(config='dev')
    app.run()
