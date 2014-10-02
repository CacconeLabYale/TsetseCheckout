from __future__ import absolute_import

# celery.py is part of the 'TsetseCheckout' package.
# It was written by Gus Dunn and was created on 9/29/14.
# 
# Please see the license info in the root folder of this package.

"""
=================================================
celery.py
=================================================
Purpose:

"""
__author__ = 'Gus Dunn'

import os

from TsetseCheckout.settings import DevConfig, ProdConfig
from TsetseCheckout.app import create_app

from celery import Celery


if os.environ.get("TSETSECHECKOUT_ENV") == 'prod':
    config_class = ProdConfig
else:
    config_class = DevConfig


def make_celery(app=None):
    app = app or create_app(config_class)

    celery = Celery(app.import_name,
                    broker=app.config['CELERY_BROKER_URL'],
                    backend=app.config['CELERY_RESULT_BACKEND'],
                    include=['TsetseCheckout.tasks'])
    celery.conf.update(app.config)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery