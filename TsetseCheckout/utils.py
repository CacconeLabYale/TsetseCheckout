# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from flask import flash


def get_file_as_string(path):
    """
    Convenience func to return contents of file as single string.
    :param path:
    :return:
    """
    with open(path, 'r') as myfile:
        return ''.join(myfile.readlines())


def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}"
                    .format(getattr(form, field).label.text, error), category)