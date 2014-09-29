# spreadsheets.py is part of the 'TsetseCheckout' package.
# It was written by Gus Dunn and was created on 9/28/14.
# 
# Please see the license info in the root folder of this package.

"""
=================================================
spreadsheets.py
=================================================
Purpose:
Handles the backend processing of checkouts initiated through the spreadsheet-upload method.
"""
__author__ = 'Gus Dunn'
import pdb

import os

import datetime as dt

from bunch import Bunch

from spartan.utils import spreadsheets as ss

from TsetseCheckout.user.models import CheckoutRequest
from TsetseCheckout.data import constants as c
from TsetseCheckout import errors as e

spreadsheets_dir = c.uploaded_spreadsheets


def get_header_indexes(worksheet):
    """
    Returns `Bunch` populated with headers as keys and col index as values.
    :param worksheet:
    :return:
    """
    header_map = Bunch()

    for index, col in enumerate(worksheet.row_values(0)):
        header_map[col] = index

    return header_map


def get_requests(upload):
    """
    Returns a generator that yields a single request at a time
    :param upload:
    :return:
    """
    date_of_request = dt.datetime.utcnow()

    expected_cols = ['to_produce',
                     'village_symbol',
                     'collection_month',
                     'collection_year',
                     'tissue_type',
                     'tube_number',
                     'new_building',
                     'new_room',
                     'new_cryo']

    rel_path = "%(bdir)s/%(fname)s" % {'bdir': spreadsheets_dir, 'fname': upload.filename}
    abs_path = os.path.abspath(rel_path)

    worksheet = ss.get_worksheets(ss.get_workbook(abs_path))[0]
    col_names_to_index = get_header_indexes(worksheet)

    rows = ss.get_row_values(worksheet)

    for row in rows:
        if 'to_produce' in row:
            continue
        else:
            pass

        request = Bunch()
        for name in expected_cols:
            try:
                i = col_names_to_index[name]
                request[name] = row[i]
            except KeyError:
                msg = "At least one of the field names in the spreadsheet request are not valid. The valid choices " \
                      "are: %(valid_names)s" % {"valid_names": str(expected_cols)}
                raise e.TsetsedbImportError(msg)

        request.username = upload.user.username
        request.date_of_request = date_of_request
        request.sample_status = 0
        request.date_approved = None
        yield CheckoutRequest(**request)


def process_requests(upload):
    """
    Attempts to load and log the requests into the CheckoutRequest table if they pass.

    Returns a list of validation failures and locations if any.
    :param upload:
    :return `list`:
    """

    validation_status = True
    request_objects = []

    # init and test validation status of requests
    for index, request in enumerate(get_requests(upload)):

        if request.validation_failures is not None:
            request_objects.append([index, request])
            validation_status = False
        else:
            request_objects.append([index, request])

    if validation_status is not False:
        # If all good, commit them to the DB
        for req in request_objects:
            req[1].save()
    else:
        pass

    return request_objects, validation_status


