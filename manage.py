# manage.py

import os
import unittest

from flask_script import Manager, Server, Command, Option
from flask_migrate import Migrate, MigrateCommand

from project.server import app, db, models

migrate = Migrate(app, db)
manager = Manager(app)

# server manager
manager.add_command("runserver", Server(host='0.0.0.0', port='8000'))

# migrations
manager.add_command('db', MigrateCommand)

@manager.command
def test():
    """Runs the unit tests"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


if __name__ == '__main__':
    manager.run()