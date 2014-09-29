# decorators.py is part of the 'TsetseCheckout' package.
# It was written by Gus Dunn and was created on 9/28/14.
# 
# Please see the license info in the root folder of this package.

"""
=================================================
decorators.py
=================================================
Purpose:

"""
__author__ = 'Gus Dunn'

from threading import Thread


def async(action):
    def wrapper(*args, **kwargs):
        thread = Thread(target=action, args=args, kwargs=kwargs)
        thread.start()
    return wrapper