import os

### Default Config Settings ###
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = 'look-a-secret-key!'

ADMINS = ['kevincrane@gmail.com']       # Administrator list

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')   # Default DB location

POSTS_PER_PAGE = 3                      # Pagination


### Prod Settings ###
if os.environ.get('APP_ENV').lower == 'prod':   # TODO: if you ever think of something better than env vars...plz
    print "Config: using 'prod' settings..."
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')    # TODO upgrade to Postgres

### Dev Settings ###
else:
    print "Config: using 'dev' settings..."
    DEBUG = True
    SQLALCHEMY_ECHO = True
    CACHE_TYPE = 'null'

    # This allows us to test the forms from WTForm
    CSRF_ENABLED = False
