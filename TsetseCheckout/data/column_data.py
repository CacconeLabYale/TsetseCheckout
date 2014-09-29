# column_data.py is part of the 'tsetseDB' package.
# It was written by Gus Dunn and was created on 2014-08-21.
#
# Please see the license info in the root folder of this package.

"""
=================================================
column_data.py
=================================================
Purpose:

"""

__author__ = 'Gus Dunn'
import re

import arrow

from TsetseCheckout import errors
from TsetseCheckout.data import constants as c

# import species abbreviation to long name dictionary
species_dict = c.get_species_abbrv_conversion_dict()

# import village to village_id conversion dict
village_id_map = c.get_village_id_map()


def convert_species_name(cell_string, file_name):
    """
    Returns expected species name format given various encountered species IDs
    from the excel files.

    :param cell_string: string containing a species
    :param file_name:
    :return: `str`
    """

    try:
        return species_dict[cell_string]
    except IndexError:
        msg = "Encountered unexpected species name '%s' in CSV file '%s'." % (cell_string, file_name)
        raise errors.TsetsedbImportError(msg)
    except:
        raise


def convert_date_dd_mm_yy(date_string, return_as="YYYY-MM-DD"):
    """
    Given a date string similar to day/month/year, return date string formatted as YYYY-MM-DD.
    :param return_as:
    :param date_string:
    :return:
    """

    valid_return_as = ('YYYY-MM-DD',
                       'datetime.date')

    if return_as not in valid_return_as:
        msg = "%s is not a valid value for `return_as`: %s" % (return_as, str(valid_return_as))
        raise ValueError(msg)

    d = date_string.lstrip("'")
    d1 = list(reversed([int(x) for x in re.findall(r"[\d']+", d)]))

    if len(str(d1[0])) >= 2:
        d1[0] += 2000

    date = arrow.get(*d1)

    if return_as == 'YYYY-MM-DD':
        return date.format("YYYY-MM-DD")
    elif return_as == 'datetime.date':
        return date.date()


def convert_tube_code(tube_string):
    """
    Given a tube_code, return the collection number alone.
    :param tube_string:
    :return:
    """
    tube_string = str(tube_string)
    digit_words = re.findall(r"[\d'\.]+", tube_string)

    return int(float(digit_words[-1]))
