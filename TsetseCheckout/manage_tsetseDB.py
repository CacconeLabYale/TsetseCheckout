#!/usr/bin/env python

# manage_tsetseDB.py is part of the 'TsetseCheckout' package.
# It was written by Gus Dunn and was created on 10/3/14.
# 
# Please see the license info in the root folder of this package.

"""
=================================================
manage_tsetseDB.py
=================================================
Purpose:
Manages migrations for the tsetseDB SAMPLE database
"""
__author__ = 'Gus Dunn'

import os
import sys
import subprocess

from flask_script import Manager, Shell
from flask_migrate import MigrateCommand

from bunch import Bunch
from flask import g
from TsetseCheckout.app import create_app
from TsetseCheckout.TsetseDB import models
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
    return {'db': db, 'models': models}


manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':

    manager.run()

