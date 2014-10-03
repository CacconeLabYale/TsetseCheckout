# database_description.py is part of the 'tsetseDB' package.
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

from datetime import datetime

from sqlalchemy import Column, ForeignKey, types
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.sql import functions as sqlalc_funcs
from sqlalchemy.engine import create_engine

from tsetseDB.utils import constants


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
        return Column(types.DateTime, nullable=False, default=datetime.now())

    @declared_attr
    def modified_when(cls):
        Column(types.DateTime, default=datetime.now())

    @declared_attr
    def needs_attention(cls):
        Column(types.Boolean, default=False, nullable=False)

    @declared_attr
    def alert_comments(cls):
        Column(types.Text)

    @declared_attr
    def comments(cls):
        Column(types.Text)


class Note(Base, MixinBase):
    """
    Table class to store notes regarding any row on any table.  The relationships will be defined in table-specific
    note-tables that record the foreign-keys of the associated row-types.
    - note_id
    - note_text
    """
    __tablename__ = 'note'
    id = Column("note_id", types.Integer, primary_key=True)
    #note_class = Column(types.Enum("history", "observation", "analysis"))
    note_text = Column(types.Text, nullable=False)


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

    infection_statuses = set(constants.infection_status_conversion.values())

    id = Column("fly_id", types.Integer, primary_key=True, nullable=False)
    fly_code = Column(types.Text, nullable=False)
    village_id = Column(types.Text, ForeignKey("village.village_id"), nullable=False)
    collection_number = Column(types.Integer)
    sex = Column(types.Enum('M', 'F'))
    species = Column(types.Enum(*constants.species_names))
    hunger_stage = Column(types.Enum('NA', '1', '2', '3', '4'))
    wing_fray = Column(types.Enum('NA', '1', '2', '3', '4'))
    box_id = Column(types.Integer, ForeignKey("box.box_id"), nullable=False)
    infected = Column(types.Boolean)
    positive_proboscis = Column(types.Enum(*infection_statuses))
    positive_midgut = Column(types.Enum(*infection_statuses))
    positive_salivary_gland = Column(types.Enum(*infection_statuses))
    tryps_by_scope = Column(types.Enum(*infection_statuses))
    tryps_by_pcr = Column(types.Boolean)
    date_of_collection = Column(types.Date)
    gps_coords = Column(types.Integer, ForeignKey("trap.gps_coords"), nullable=False)
    teneral = Column(types.Boolean)
    comments = Column(types.Text)


class FlyNote(Base, MixinBase):
    """
    Table class to store relationships between which rows in "note" table pertain to which rows in "fly" table.
    - fly_note_id
    - fly_id
    """
    __tablename__ = 'fly_note'
    id = Column("fly_note_id", types.Integer, primary_key=True, nullable=False)
    fly_id = Column(types.Integer, ForeignKey("fly.fly_id"), nullable=False)


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
    id = Column("village_id", types.Text, primary_key=True)
    district = Column(types.Text)
    county = Column(types.Text)
    subcounty = Column(types.Text)
    parish = Column(types.Text)
    village_name = Column(types.Text)


class VillageNote(Base, MixinBase):
    """
    Table class to store relationships between which rows in "note" table pertain to which rows in "village" table.
    - village_note_id
    - village_id
    """
    __tablename__ = 'village_note'
    id = Column("village_note_id", types.Integer, primary_key=True, nullable=False)
    village_id = Column(types.Text, ForeignKey("village.village_id"), nullable=False)


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
    # id = Column("trap_id", types.Text, primary_key=True)
    trap_number = Column(types.Integer)
    season = Column(types.Enum('wet', 'dry'))
    deploy_date = Column(types.Date)
    removal_date = Column(types.Date)
    trap_type = Column(types.Enum('biconical'))
    village_id = Column(types.Text, ForeignKey("village.village_id"), nullable=False)
    gps_coords = Column(types.Text, primary_key=True)
    elevation = Column(types.Float)
    veg_type = Column(types.Text)
    other_info = Column(types.Text)


class TrapNote(Base, MixinBase):
    """
    Table class to store relationships between which rows in "note" table pertain to which rows in "trap" table.
    - trap_note_id
    - gps_coords
    """
    __tablename__ = 'trap_note'
    id = Column("trap_note_id", types.Integer, primary_key=True, nullable=False)
    gps_coords = Column(types.Integer, ForeignKey("trap.gps_coords"), nullable=False)
    

class Tube(Base, MixinBase):
    """
    Table class to store data associated with a single storage tube:
    - contents
    - solution
    - fly_id
    """
    __tablename__ = 'tube'
    id = Column("tube_id", types.Integer, primary_key=True)
    contents = Column(types.Enum('midgut',
                                 'salivary gland',
                                 'reproductive parts',
                                 'carcass',
                                 'intact fly',
                                 'DNA',
                                 'RNA'))
    solution = Column(types.Text)
    fly_id = Column(types.Integer, ForeignKey("fly.fly_id"))
    box_id = Column(types.Integer, ForeignKey("box.box_id"))
    parent_id = Column(types.Integer, ForeignKey("tube.tube_id"))


class TubeNote(Base, MixinBase):
    """
    Table class to store relationships between which rows in "note" table pertain to which rows in "tube" table.
    - tube_note_id
    - tube_id
    """
    __tablename__ = 'tube_note'
    id = Column("tube_note_id", types.Integer, primary_key=True, nullable=False)
    tube_id = Column(types.Integer, ForeignKey("tube.tube_id"), nullable=False)


class Box(Base, MixinBase):
    """
    Table class to store data associated with a freezer box where tubes are stored:
    - freezer
    - room
    - freezer_loc
    """
    __tablename__ = 'box'
    id = Column("box_id", types.Integer, primary_key=True)
    room = Column(types.Text)
    freezer = Column(types.Text)
    freezer_loc = Column(types.Text)


class BoxNote(Base, MixinBase):
    """
    Table class to store relationships between which rows in "note" table pertain to which rows in "box" table.
    - box_note_id
    - box_id
    """
    __tablename__ = 'box_note'
    id = Column("box_note_id", types.Integer, primary_key=True, nullable=False)
    box_id = Column(types.Integer, ForeignKey("box.box_id"), nullable=False)



