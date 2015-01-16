# models.py is part of the 'TsetseCheckout' package.
# It was written by Gus Dunn and was created on Thu Aug 14 17:31:36 EDT 2014.
#
# Please see the license info in the root folder of this package.

"""
=================================================
database_description.py
=================================================
Purpose:

"""

__author__ = 'Gus Dunn'

import datetime as dt

from bunch import Bunch
from flask_login import UserMixin

from TsetseCheckout.extensions import bcrypt
from TsetseCheckout.database import (
    Column,
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
)

from TsetseCheckout.data import validation as qc
from TsetseCheckout import errors as e





from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.engine import create_engine

from TsetseCheckout.data import constants as c


Base = declarative_base()


def get_engine(db_uri, echo=False, checkfirst=True):
    """

    :param db_uri:
    :param echo:
    :param checkfirst:
    :return:
    """
    engine = create_engine(db_uri, echo=echo)
    Base.metadata.create_all(bind=engine, checkfirst=checkfirst)

    return engine, Base.metadata


# noinspection PyDocstring
class MixinBase(object):
    @declared_attr
    def created_when(cls):
        return Column(db.DateTime, nullable=False, default=dt.datetime.now())

    @declared_attr
    def modified_when(cls):
        Column(db.DateTime, default=dt.datetime.now())

    @declared_attr
    def needs_attention(cls):
        Column(db.Boolean, default=False, nullable=False)

    @declared_attr
    def alert_comments(cls):
        Column(db.Text)

    @declared_attr
    def comments(cls):
        Column(db.Text)


class Note(Base, MixinBase):
    """
    Table class to store notes regarding any row on any table.  The relationships will be defined in table-specific
    note-tables that record the foreign-keys of the associated row-types.
    - note_id
    - note_text
    """
    __tablename__ = 'note'
    id = Column("note_id", db.Integer, primary_key=True)
    #note_class = Column(db.Enum("history", "observation", "analysis"))
    note_text = Column(db.Text, nullable=False)


class Fly(Base, MixinBase):
    """
    Table class to store data associated with individual flies:
    - id (int)
    - fly_code (str)
    - village_id (str)
    - collection_number (int)
    - sex (M|F)
    - species (f|p|m)
    - hunger_stage (1|2|3)
    - wing_fray (int)
    - box_id (ForeignKey?)
    - infected (bool)
    - tryps_by_scope (bool)
    - tryps_by_pcr (bool)
    - date_of_collection (date)
    - gps_coords (int, ForeignKey?)
    - gps_coords (link to TrapTable) (or would I just do a specific join whenever I want this?)
    - teneral (bool)
    - comments (str)
    """
    __tablename__ = 'fly'

    infection_statuses = set(c.infection_status_conversion.values())

    id = Column("fly_id", db.Integer, primary_key=True, nullable=False)
    fly_code = Column(db.Text, nullable=False)
    village_id = Column(db.Text, ForeignKey("village.village_id"), nullable=False)
    collection_number = Column(db.Integer)
    sex = Column(db.Enum('M', 'F'))
    species = Column(db.Enum(*c.species_names))
    hunger_stage = Column(db.Enum('NA', '1', '2', '3', '4'))
    wing_fray = Column(db.Enum('NA', '1', '2', '3', '4'))
    box_id = Column(db.Integer, ForeignKey("box.box_id"), nullable=False)
    infected = Column(db.Boolean)
    positive_proboscis = Column(db.Enum(*infection_statuses))
    positive_midgut = Column(db.Enum(*infection_statuses))
    positive_salivary_gland = Column(db.Enum(*infection_statuses))
    tryps_by_scope = Column(db.Enum(*infection_statuses))
    tryps_by_pcr = Column(db.Boolean)
    date_of_collection = Column(db.Date)
    gps_coords = Column(db.Integer, ForeignKey("trap.gps_coords"), nullable=False)
    teneral = Column(db.Boolean)
    comments = Column(db.Text)


class FlyNote(Base, MixinBase):
    """
    Table class to store relationships between which rows in "note" table pertain to which rows in "fly" table.
    - fly_note_id
    - fly_id
    """
    __tablename__ = 'fly_note'
    id = Column("fly_note_id", db.Integer, primary_key=True, nullable=False)
    fly_id = Column(db.Integer, ForeignKey("fly.fly_id"), nullable=False)


class Village(Base, MixinBase):
    """
    Table class to store data associated with a single village:
    - id (int)
    - district
    - county
    - subcounty
    - parish
    - village_name

    """
    __tablename__ = 'village'
    id = Column("village_id", db.Text, primary_key=True)
    district = Column(db.Text)
    county = Column(db.Text)
    subcounty = Column(db.Text)
    parish = Column(db.Text)
    village_name = Column(db.Text)


class VillageNote(Base, MixinBase):
    """
    Table class to store relationships between which rows in "note" table pertain to which rows in "village" table.
    - village_note_id
    - village_id
    """
    __tablename__ = 'village_note'
    id = Column("village_note_id", db.Integer, primary_key=True, nullable=False)
    village_id = Column(db.Text, ForeignKey("village.village_id"), nullable=False)


class Trap(Base, MixinBase):
    """
    Table class to store data associated with a single trap:
    - id (int)
    - season (wet|dry)
    - deploy_date
    - removal_date
    - trap_type (biconical|other?)
    - village_id (ForgnKey?)
    - gps_coords (Text)
    - elevation (float)
    """
    __tablename__ = 'trap'
    # id should be "%s:%s" % (deploy_date, gps_coords)
    # id = Column("trap_id", db.Text, primary_key=True)
    trap_number = Column(db.Integer)
    season = Column(db.Enum('wet', 'dry'))
    deploy_date = Column(db.Date)
    removal_date = Column(db.Date)
    trap_type = Column(db.Enum('biconical'))
    village_id = Column(db.Text, ForeignKey("village.village_id"), nullable=False)
    gps_coords = Column(db.Text, primary_key=True)
    elevation = Column(db.Float)
    veg_type = Column(db.Text)
    other_info = Column(db.Text)


class TrapNote(Base, MixinBase):
    """
    Table class to store relationships between which rows in "note" table pertain to which rows in "trap" table.
    - trap_note_id
    - gps_coords
    """
    __tablename__ = 'trap_note'
    id = Column("trap_note_id", db.Integer, primary_key=True, nullable=False)
    gps_coords = Column(db.Integer, ForeignKey("trap.gps_coords"), nullable=False)
    

class Tube(Base, MixinBase):
    """
    Table class to store data associated with a single storage tube:
    - contents
    - solution
    - fly_id
    """
    __tablename__ = 'tube'
    id = Column("tube_id", db.Integer, primary_key=True)
    contents = Column(db.Enum('midgut',
                                 'salivary gland',
                                 'reproductive parts',
                                 'carcass',
                                 'intact fly',
                                 'DNA',
                                 'RNA'))
    solution = Column(db.Text)
    fly_id = Column(db.Integer, ForeignKey("fly.fly_id"))
    box_id = Column(db.Integer, ForeignKey("box.box_id"))
    parent_id = Column(db.Integer, ForeignKey("tube.tube_id"))


class TubeNote(Base, MixinBase):
    """
    Table class to store relationships between which rows in "note" table pertain to which rows in "tube" table.
    - tube_note_id
    - tube_id
    """
    __tablename__ = 'tube_note'
    id = Column("tube_note_id", db.Integer, primary_key=True, nullable=False)
    tube_id = Column(db.Integer, ForeignKey("tube.tube_id"), nullable=False)


class Box(Base, MixinBase):
    """
    Table class to store data associated with a freezer box where tubes are stored:
    - freezer
    - room
    - freezer_loc
    """
    __tablename__ = 'box'
    id = Column("box_id", db.Integer, primary_key=True)
    room = Column(db.Text)
    freezer = Column(db.Text)
    freezer_loc = Column(db.Text)


class BoxNote(Base, MixinBase):
    """
    Table class to store relationships between which rows in "note" table pertain to which rows in "box" table.
    - box_note_id
    - box_id
    """
    __tablename__ = 'box_note'
    id = Column("box_note_id", db.Integer, primary_key=True, nullable=False)
    box_id = Column(db.Integer, ForeignKey("box.box_id"), nullable=False)



