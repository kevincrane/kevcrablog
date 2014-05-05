#!/usr/bin/env python
import os
from flask import Flask
from flask.ext.admin import Admin
from flask.ext.admin.contrib.fileadmin import FileAdmin
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.misaka import Misaka
from flask.ext.moment import Moment

from app.core import db
from app.admin import AdminMain, PostAdminView, NewPostView
from app.kevcrablog import views

# from flask.ext.cache import Cache     # TODO add caching
# Setup flask cache
# cache = Cache()       # TODO add caching

# init flask assets
# assets_env = Environment()    # TODO assets?
from app.kevcrablog.models import Post
from settings import BASE_DIR


def create_app(config='dev'):
    """ Flask application factory
    :param config: type of app to build, either "prod" or "dev"
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

    # Init the cache
    # cache.init_app(app)       # TODO add caching

    Moment(app)         # moment.js
    Misaka(app, autolink=True, # Misaka Markdown
           fenced_code=True, lax_html=True, strikethrough=True,
           superscript=True, tables=True, wrap=True)

    # Init Admin page
    admin = Admin(app)
    # admin.add_view(AdminMain(name="Admin"))
    admin.add_view(PostAdminView())
    admin.add_view(NewPostView())
    static_path = os.path.join(BASE_DIR, 'app', 'static')
    admin.add_view(FileAdmin(static_path, '/static/', name='Static Files'))

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
