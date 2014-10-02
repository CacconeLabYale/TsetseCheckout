#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import subprocess

from flask_script import Manager, Shell, Server
from flask.ext.migrate import MigrateCommand

from bunch import Bunch
from flask import g
from TsetseCheckout.app import create_app
from TsetseCheckout.user import models
from TsetseCheckout.settings import DevConfig, ProdConfig
from TsetseCheckout.database import db

if os.environ.get("TSETSECHECKOUT_ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)



# Make calling extensions take less typing
app.extensions = Bunch(app.extensions)

manager = Manager(app)
TEST_CMD = "py.test tests"


def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and user.models model by default.
    """
    return {'app': app, 'db': db, 'models': models}


@manager.command
def test():
    """Run the tests."""
    import pytest
    exit_code = pytest.main(['tests', '--verbose'])
    return exit_code


@manager.command
def get_app():
    """
    Returns `app`.
    Useful for getting a fully initialized app instance for debugging in ipython.
    """
    return app

manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':

    manager.run()

