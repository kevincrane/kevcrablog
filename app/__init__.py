#! ../env/bin/python
import os

from flask import Flask
# from flask.ext.cache import Cache     # TODO add caching
from app.core import db
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.moment import Moment
from app.kevcrablog import views

# Setup flask cache
# cache = Cache()       # TODO add caching

# init flask assets
# assets_env = Environment()    # TODO assets?


def create_app(config_file, env="dev"):
    """ Flask application factory
    :param config_file: filename/classpath of config file
    :param env: type of app to build, either "prod" or "dev"
    """
    # Create flask application
    app = Flask(__name__)
    app.config.from_object(config_file)
    app.config['ENV'] = env

    # Debug toolbar (when debug=true)
    debug_toolbar = DebugToolbarExtension(app)
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.config['DEBUG_TB_PROFILER_ENABLED'] = True

    # Register Blueprints
    app.register_blueprint(views.blog)

    # Init the cache
    # cache.init_app(app)       # TODO add caching

    # Init moment.js
    moment = Moment(app)

    # Init DB
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
    env = os.environ.get('APP_ENV', 'dev')     # TODO change this to be easier?
    app = create_app('app.settings.%sConfig' % env.capitalize(), env=env)
    app.run()
