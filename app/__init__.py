#!/usr/bin/env python
import os

from flask import Flask
from flask.ext.admin import Admin
from flask.ext.babel import Babel
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.misaka import Misaka
from flask.ext.moment import Moment
from flask.ext.user import UserManager, SQLAlchemyAdapter
from flask.ext.cache import Cache     # TODO add caching

from app.core import db
from app.admin import AdminMain, PostAdminView, NewPostView, FileAdminView

cache = Cache(config={'CACHE_TYPE': 'simple'})
from app.kevcrablog import views

from app.kevcrablog.models import Post
from app.models import User
from settings import BASE_DIR

# init flask assets
# assets_env = Environment()    # TODO assets?


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
    app.register_blueprint(views.blog)

    # Set up Flask-User
    babel = Babel(app)
    db_adapter = SQLAlchemyAdapter(db, User)
    user_manager = UserManager(db_adapter, app)     # Init Flask-User and bind to app

    # Init the cache

    cache.init_app(app)

    Moment(app)         # moment.js
    Misaka(app, autolink=True, # Misaka Markdown
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

    # Import and register the different asset bundles
    """ TODO: assets and blueprints?
    assets_env.init_app(app)
    assets_loader = PythonAssetsLoader(assets)
    for name, bundle in assets_loader.load_bundles().iteritems():
        assets_env.register(name, bundle)
    """
    return app


if __name__ == '__main__':
    app = create_app(config='dev')
    app.run()
