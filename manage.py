#!/usr/bin/env python
import os
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server
from app import create_app, db
from app.kevcrablog import models


description_msg = "The Kevin Crane personal site (for prod: export APP_ENV=prod)"

env = os.environ.get('APP_ENV', 'dev')
app = create_app(env)

manager = Manager(app, description=description_msg, with_default_commands=False)
manager.add_command('server', Server(use_debugger=app.debug))
manager.add_command('db', MigrateCommand)
migrate = Migrate(app, db)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, models=models)


if __name__ == "__main__":
    manager.run()
