from contextlib import contextmanager
from datetime import date
from fabric.api import *
from fabric.colors import cyan, red, green, yellow
from fabric.context_managers import settings, cd, prefix
from fabric.contrib.files import append
from fabric.state import env


env.hosts = ['kcrane.co']
env.user = 'kevin'
env.proj_root = '/opt/sites/thekevincrane'
env.activate = 'source %s/venv/bin/activate' % env.proj_root
env.repo = 'https://github.com/kevincrane/kevcrablog.git'
env.pg_db = 'thekevincrane'
env.local_db_backup = '~/.thekevincrane/db_backups'


@contextmanager
def virtualenv():
    with cd(env.proj_root):
        with prefix('source venv/bin/activate'):
            yield


def set_permissions(directory, user='www-data', group='www-data'):
    """ Set ownership permissions of a whole directory
    """
    sudo('chown -R %s:%s %s' % (user, group, directory))


##### Fab Tasks Below #####

@task
def install():
    """ Fully set up a brand new Ubuntu production environment from scratch
    """
    # Creating remote user if applicable
    print(cyan('Creating remote user %s...' % env.user))
    temp_user = env.user
    env.user = 'root'
    if sudo('id %s' % temp_user, warn_only=True).failed:
        sudo('adduser %s' % temp_user)
        sudo('echo "%s	ALL=(ALL:ALL) ALL" >> /etc/sudoers' % temp_user)
    env.user = temp_user

    # Install packages
    print(cyan('Updating Ubuntu packages to most recent version...'))
    sudo('add-apt-repository ppa:certbot/certbot')
    sudo('apt-get update && apt-get -y upgrade')
    print(cyan('Downloading important programs (servers and databases and python and shit)...'))
    sudo('apt-get install  -y build-essential python python-dev git python-pip python-virtualenv fail2ban '
         'python-certbot-nginx  postgresql postgresql-contrib libpq-dev nginx uwsgi uwsgi-plugin-python')

    # Configure log location
    print(cyan('Creating uwsgi log location...'))
    sudo('mkdir -p /var/log/thekevincrane')
    sudo('chown www-data:www-data /var/log/thekevincrane')

    # Create application directories and fetch the repo
    print(cyan('Installing full application...'))
    pull()
    update_deps()
    set_permissions(env.proj_root)

    # Configure nginx, uwsgi, and postgres
    configure()
    print(green('Finished installing production system (%s)!' % env.host))


@task
def configure():
    """ Set up the right configurations for uwsgi, nginx, and postgres
    """
    print(cyan('Moving to nginx and uwsgi config files to their /etc homes...'))
    with settings(warn_only=True):
        # disable default site
        sudo('rm -f /etc/nginx/sites-enabled/default')
        sudo('cp %s/ops/thekevincrane_nginx.conf /etc/nginx/sites-available/thekevincrane' % env.proj_root)
        sudo('ln -sf /etc/nginx/sites-available/thekevincrane /etc/nginx/sites-enabled/thekevincrane')

        sudo('cp %s/ops/thekevincrane_uwsgi.ini /etc/uwsgi/apps-available/thekevincrane.ini' % env.proj_root)
        sudo('ln -sf /etc/uwsgi/apps-available/thekevincrane.ini /etc/uwsgi/apps-enabled/thekevincrane.ini')

        # TODO: set up non-Upstart option if upstart not available (probably in /etc/uwsgi/apps-available)
        sudo('cp %s/ops/thekevincrane_upstart.conf /etc/init/thekevincrane.conf' % env.proj_root)
        sudo('cp %s/ops/thekevincrane_systemd.conf /etc/systemd/system/thekevincrane.service' % env.proj_root)

        sudo('certbot --nginx -d kcrane.co -n')  # set up Let's Encrypt
        sudo('cp %s/ops/certbot_renew.cron /etc/cron.monthly/certbot_renew' % env.proj_root)

    # Set up Postgres and secret keys
    pg_uname, pg_pword = instance_config()
    config_db(pg_uname, pg_pword)

    # Restart appropriate services
    reload()
    print(green('Finished configuring a new production environment!'))


@task
def config_db(pg_uname=None, pg_pword=None):
    """ Initialize Postgres DB for thekevincrane
    """
    print(cyan('Configuring Postgres...'))
    if not pg_uname:
        pg_uname = prompt('Enter a username for Postgres:', default=env.user, validate=r'^[^\']*$')
    # Check if username exists before trying to create new one
    if sudo('psql -tAc "SELECT 1 FROM pg_roles WHERE rolname=\'%s\'" | grep -q 1' % pg_uname,
            user='postgres', quiet=True).succeeded:
        print(yellow('Postgres user %s already exists, skipping.' % pg_uname))
    else:
        if not pg_pword:
            pg_pword = prompt('Enter a password for Postgres user %s:' % pg_uname, validate=r'^[^\']*$')
        sudo('psql -c "CREATE USER %s WITH CREATEDB PASSWORD \'%s\';"' % (pg_uname, pg_pword), user='postgres')

    # Check if database exists before trying to create new one
    if sudo('psql -tAc "SELECT 1 FROM pg_catalog.pg_database WHERE datname = \'%s\';" | grep -q 1' % env.pg_db,
            user='postgres', quiet=True).succeeded:
        print(yellow('Postgres database %s already exists, skipping.' % env.pg_db))
    else:
        sudo('psql -c "CREATE DATABASE %s"' % env.pg_db, user='postgres')
    print(cyan('Restarting Postgres...'))
    sudo('service postgresql restart')

    print(cyan('Creating initial database tables...'))
    with virtualenv():
        sudo("echo 'db.create_all()' | APP_ENV=prod ./manage.py shell", warn_only=True)
        sudo("echo 'db.create_all()' | APP_ENV=dev ./manage.py shell", warn_only=True)
    print(green('Finishing configuring Postgres!'))


@task
def instance_config():
    """ Create instance config file for secret values that should only exist on production (out of version control)
    """
    print(cyan('Saving secret instance config values...'))
    # Prompt for secret values; regex blocks any strings with single quotes in them
    secret_key = prompt('What should our secret key be?', validate=r'^[^\']*$')
    pg_uname = prompt('What user will log on to Postgres?', default=env.user, validate=r'^[^\']*$')
    pg_pword = prompt('What is the Postgres password for %s?' % pg_uname, validate=r'^[^\']*$')
    sudo('mkdir -p %s/instance' % env.proj_root)
    instance_configuration = """# WARNING: Don't change this file unless you know what you're doing!
#          Will eventually be automatically overwritten by Fabric
SECRET_KEY = '%s'
PG_UNAME = '%s'
PG_PWORD = '%s'
""" % (secret_key, pg_uname, pg_pword)
    sudo('rm -f %s/instance/__init__.py' % env.proj_root)
    append('%s/instance/__init__.py' % env.proj_root, instance_configuration, use_sudo=True)
    print(green('Saved secret configurations to %s/instance/__init__.py!' % env.proj_root))
    return pg_uname, pg_pword   # For use by config_db() if necessary


@task
def reload():
    """ Reload nginx and uwsgi servers
    """
    print(cyan('Restarting nginx and uwsgi...'))
    sudo('service nginx restart')
    sudo('service thekevincrane restart')
    print(green('Servers are reloaded!'))


def init_pull():
    """ Initial git pull, need to install deps and initialize migration
    """
    print(cyan("Fetching code from GitHub..."))
    sudo('mkdir -p /opt/sites')
    sudo('git clone %s %s' % (env.repo, env.proj_root))
    print(cyan("Creating new virtualenv and installing dependencies..."))
    sudo('virtualenv --no-site-packages %s/venv' % env.proj_root)
    update_deps()
    print(cyan('Creating initial DB migration...'))
    with virtualenv():
        sudo('./manage.py db init')
    print(green('Initial codebase instantiated!'))


@task
def pull():
    """ Update code from git on production
    """
    # Create project root, fetch the code and virtualenv
    if run("test -d %s" % env.proj_root, warn_only=True).failed:
        init_pull()
    with cd(env.proj_root):
        print(cyan('Pulling latest code from master...'))
        sudo('git pull origin master')
    print(green('Finished deploying latest code!'))


def update_deps():
    """ Update python dependencies for thekevincrane
    """
    with virtualenv():
        sudo('pip install -r requirements.txt')


@task
def migrate():
    """ Local: Update DB to latest migration version from model changes
    """
    msg = prompt('What changes did you make to the models?')
    with prefix('source venv/bin/activate'):
        result = local('./manage.py db migrate -m "%s"' % msg)
        if result.failed:
            print(yellow('Migration failed, trying to upgrade DB to latest version.'))
            local('./manage.py db upgrade')
            print(yellow('Upgrade successful, please retry the migration!'))
        else:
            print(green('Finished migrating DB models!'))


def migration_up():
    """ Update DB to latest migration version
    """
    with virtualenv():
        sudo('APP_ENV=prod ./manage.py db upgrade')
        sudo('APP_ENV=dev ./manage.py db upgrade')
    print(green('Updated remote DB to latest version!'))


@task
def deploy():
    """ Deploy latest version of the app to production
    """
    print(cyan('Deploying latest version to production...'))
    pull()
    update_deps()
    migration_up()
    reload()
    print(green('Remote application is up to date!'))


@task
def backup_db():
    """ Create a backup of the remote database and copy it locally (see comments for how to restore)
    """
    # Can restore with:
    #   pg_restore --dbname=thekevincrane --create --verbose thekevincrane-DATE.tar
    #   psql -d thekevincrane -f thekevincrane-DATE.dump    # if plaintext SQL file
    print(cyan('Backing up remote database...'))
    backup_date = date.today()
    with virtualenv():
        sudo('mkdir -p %s/backups' % env.proj_root)
        sudo('chown postgres:postgres %s/backups' % env.proj_root)
        sudo('pg_dump -F t %s > %s/backups/thekevincrane-%s.tar' %
             (env.pg_db, env.proj_root, backup_date), user='postgres')
    print(cyan('Fetching new DB backup...'))
    local('mkdir -p %s' % env.local_db_backup)
    get(remote_path='%s/backups/thekevincrane-%s.tar' % (env.proj_root, backup_date),
        local_path='%s/' % env.local_db_backup)
    print(green('Backup saved to %s/%s!' % (env.local_db_backup, backup_date)))


# @task
def reboot():
    """ Reboot the remote system after 30 seconds (Doesn't work)
    """
    # TODO: fix this
    reboot(wait=30)


@task
def shell():
    """ Open a terminal to the playground
    """
    open_shell()


@task
def run_local():
    """ Local: Run a local Flask server for development
    """
    with prefix('source venv/bin/activate'):
        local('APP_ENV=dev ./manage.py server')


# TODO: add local git commit/push task


@task
def run_dev():
    """ Run a remote development version of the application
    """
    with virtualenv():
        sudo('APP_ENV=dev uwsgi --plugins python --http-socket :8080 --chdir %s --home venv --module manage:app'
             % env.proj_root)
