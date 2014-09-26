from flask.ext.uploads import UploadSet
from bunch import Bunch
import settings

# Set file groups of types of files allowed to upload by users in certain cases
upload_sets = Bunch()

upload_sets.spreadsheets = UploadSet(name='spreadsheet', extensions=tuple("xls xlsx ods".split()),
                                     default_dest=None)