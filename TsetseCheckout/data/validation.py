# data_validation.py is part of the 'TsetseCheckout' package.
# It was written by Gus Dunn and was created on 9/27/14.
# 
# Please see the license info in the root folder of this package.

"""
=================================================
validation.py
=================================================
Purpose:
Stores code to validate user input and other important information.
"""
__author__ = 'Gus Dunn'

import datetime as dt

import TsetseCheckout.user as user
from TsetseCheckout.data import constants as c
from TsetseCheckout.data import column_data as cd
from TsetseCheckout import errors as e


def username_exists(username):

    if username in [u.username for u in user.models.User.query.all()]:
        return username
    else:
        msg = "%(uname)s is not a valid username." % {'uname': username}
        raise e.TsetsedbImportError(msg)


def valid_fly_derivatives(derivative):

    if derivative.upper() in c.fly_derivatives:
        return derivative.upper()
    else:
        msg = "%(deriv)s is not an expected material to produce from the fly samples.  Choose from: %(opts)s" \
              % {"deriv": derivative,
                 "opts": str(c.fly_derivatives)}
        raise e.TsetsedbImportError(msg)


def valid_tissue_type(tissue_type):
    if tissue_type.upper() in c.fly_tissue_types:
        return tissue_type.upper()
    else:
        msg = "%(tis)s is not a recognized tissue type: %(types)s." % {"tis": tissue_type, "types": c.fly_tissue_types}
        raise e.TsetsedbImportError(msg)


def valid_village_id(village_id):

    if village_id.upper() in c.get_village_ids():
        return village_id.upper()
    else:
        msg = "%(vil)s is not a recognized village id." % {"vil": village_id}
        raise e.TsetsedbImportError(msg)


def valid_month(month):
    if month in c.months:
        return month
    else:
        try:  # Converting from short word to number (Mar to 3)
            return dt.datetime.strptime(month, "%b").month
        except ValueError:
            try:  # Converting from long word to number (March to 3)
                return dt.datetime.strptime(month, "%B").month
            except ValueError:
                msg = "%(month)s is not a recognized representation of a month of the year" % {"month": month}
                raise e.TsetsedbImportError(msg)


def valid_year(year):
    year = int(year)
    if year in c.years:
        return year
    else:
        msg = "%(year)s is not a valid year for this collection." % {"year": year}
        raise e.TsetsedbImportError(msg)


def valid_tube_number(tube_number):
    try:
        return cd.convert_tube_code(tube_number)
    except IndexError:
        msg = "I was not able to translate '%(tube_number)s' into a tube number." % {"tube_number": tube_number}
        raise e.TsetsedbImportError(msg)


def valid_building_code(building_code):
    if building_code in c.get_building_codes():
        return building_code
    else:
        msg = "%(code)s is not present in our list of building codes.  Please contact the administrator of the " \
              "database." % {"code": building_code}
        raise e.TsetsedbImportError(msg)


def valid_sample_status(status):
    if status in c.sample_statuses.values():
        return status
    else:
        msg = "The status code '%(status)s is not valid. Choose from the numbers in: %(codes)s." \
              % {'status': status, 'codes': c.sample_statuses}
        raise e.TsetsedbImportError(msg)
