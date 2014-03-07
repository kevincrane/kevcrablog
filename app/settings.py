import os

# TODO: replace with list of properties rather than classes
# TODO: replace this with separate files for dev/prod


class Config(object):
    """ Base Config for everything
    """
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = 'secret key'

    # Administrator list
    ADMINS = ['kevincrane@gmail.com']

    # pagination
    POSTS_PER_PAGE = 5


class ProdConfig(Config):
    """ Prod Config object
    """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(Config.BASE_DIR, 'app.db')    # TODO upgrade to Postgres

    CACHE_TYPE = 'simple'


class DevConfig(Config):
    """ Dev Config object
    """
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(Config.BASE_DIR, 'app.db')
    SQLALCHEMY_ECHO = True

    CACHE_TYPE = 'null'

    # This allows us to test the forms from WTForm
    CSRF_ENABLED = False
