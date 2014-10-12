import os

### Default Config Settings ###
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = 'look-a-secret-key!'       # Not real, gets overwritten in production

ADMINS = ['kevincrane@gmail.com']       # Administrator list

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')   # Default DB location

POSTS_PER_PAGE = 5                      # Pagination

# Flask-User settings
USER_ENABLE_EMAIL = False
USER_ENABLE_REGISTRATION = False        # Change this to true to add users again!


### Prod Settings ###
if os.environ.get('APP_ENV') == 'prod':   # TODO: if you ever think of something better than env vars...plz
    print "Config: using 'prod' settings..."
    DEBUG = False

    # Load secret instance config values
    try:
        import instance
        SQLALCHEMY_DATABASE_URI = "postgres://%s:%s@localhost:5432/thekevincrane" % \
                                  (instance.PG_UNAME, instance.PG_PWORD)
    except ImportError:
        print "Error: could not load secret instance configuration values!'"

### Dev Settings ###
else:
    print "Config: using 'dev' settings..."
    DEBUG = True
    SQLALCHEMY_ECHO = True
    CACHE_TYPE = 'null'

    # This allows us to test the forms from WTForm
    CSRF_ENABLED = False
