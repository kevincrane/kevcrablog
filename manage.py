#!/usr/bin/env python
import os

from flask.ext.script import Manager, Server
from app import create_app
from app.kevcrablog.models import db, User


env = os.environ.get('APP_ENV', 'dev')
app = create_app('app.settings.%sConfig' % env.capitalize(), env=env)

manager = Manager(app)
manager.add_command("server", Server())     # TODO: prod server? look at Server code in this class <--Server()

#TODO: MigrateCommand


@manager.shell
def make_shell_context():
    """ Creates a python REPL with several default imports
    in the context of the app
    """
    return dict(app=app, User=User)


@manager.command
def createdb():
    """ Creates a database with all of the tables defined in
    your Alchemy models
    """
    db.create_all()


if __name__ == "__main__":
    manager.run()
