# tasks.py is part of the 'TsetseCheckout' package.
# It was written by Gus Dunn and was created on 9/29/14.
# 
# Please see the license info in the root folder of this package.

"""
=================================================
tasks.py
=================================================
Purpose:

"""
__author__ = 'Gus Dunn'

from flask import current_app, g

from TsetseCheckout.celery import make_celery

celery = make_celery(current_app)


@celery.task()
def add_together(a, b):
    return a + b