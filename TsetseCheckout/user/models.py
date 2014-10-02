# -*- coding: utf-8 -*-
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


class CheckoutRequest(SurrogatePK, Model):
    __tablename__ = "checkout_requests"

    username = Column(db.String(80), db.ForeignKey('users.username'))
    to_produce = Column(db.String(60), nullable=False)  # TODO: add validation
    village_symbol = Column(db.String(15), nullable=False)  # TODO: add validation
    collection_month = Column(db.Integer(), nullable=False)  # TODO: add validation
    collection_year = Column(db.Integer(), nullable=False)  # TODO: add validation
    tissue_type = Column(db.String(15), default="OTHER", nullable=False)  # TODO: add validation
    tube_number = Column(db.Integer, nullable=False)  # TODO: add validation
    date_of_request = Column(db.DateTime, nullable=False)
    date_approved = Column(db.DateTime, nullable=True)
    new_building = Column(db.String(5), nullable=False)  # TODO: add validation
    new_room = Column(db.String(8), nullable=False)
    new_cryo = Column(db.String(30), nullable=False)
    sample_status = Column(db.String(15), nullable=False)  # TODO: add validation
    # passed_validation = Column(db.Boolean, nullable=True)

    def __init__(self, username, to_produce, village_symbol, collection_month, collection_year, tissue_type,
                 tube_number, new_building, new_room, new_cryo, sample_status=0, date_approved=None,
                 date_of_request=dt.datetime.utcnow(),
                 **kwargs):

        self.validation_failures = None
        self.tube_available = None

        columns = Bunch(username=username, to_produce=to_produce, village_symbol=village_symbol,
                        collection_month=collection_month, collection_year=collection_year, tissue_type=tissue_type,
                        tube_number=tube_number, date_of_request=date_of_request, date_approved=date_approved,
                        new_building=new_building, new_room=new_room, new_cryo=new_cryo, sample_status=sample_status)

        validated_columns = self._validate_columns(columns)

        # run parent class __init__ to populate `self`
        db.Model.__init__(self, **validated_columns)

        # confirm tube is available and update the switches
        self._tube_is_available()

    def _tube_is_available(self):
        """
        Sets `self.tube_available` to `False` and record error message if a previous request exists or the tube is
        listed as unavail in the tsetseSampleDB.
        :return:
        """

        if any([self._existing_requests(),
                self._tube_is_checkedout()]):  # TODO: The main DB is NOT connected to this website yet!

            self.tube_available = False
            try:
                self.validation_failures["TubeNotAvailable"] = "This tube seems to have been requested already or is " \
                                                               "not available according to the main sampleDB."
            except TypeError:
                self.validation_failures = Bunch()
                self.validation_failures["TubeNotAvailable"] = "This tube seems to have been requested already or is " \
                                                               "not available according to the main sampleDB."
        else:
            self.tube_available = True

    def _tube_is_checkedout(self):
        """
        Returns `False` if tube IS available in main DB.
        :return:
        """
        # TODO: CONNECT TO MAIN DB and write REAL code here

        return False

    def _existing_requests(self):
        """
        Returns `True` if a request for this already exists.
        :return:
        """
        reqs = self.query.filter_by(village_symbol=self.village_symbol, collection_month=self.collection_month,
                                    collection_year=self.collection_year, tube_number=self.tube_number).all()

        if len(reqs) > 0:
            return True
        else:
            return False

    # TODO: look at using sqlalchemy 'listeners' for automated EVERY-TIME validations
    def _validate_columns(self, columns_bunch):

        """
        Handles preliminary data validation of column values.
        :param columns_bunch:
        :return:
        """
        c = columns_bunch
        exceptions = Bunch()
        validated = Bunch()
        validation_funcs = Bunch({"username": qc.username_exists,
                                  "to_produce": qc.valid_fly_derivatives,
                                  "village_symbol": qc.valid_village_id,
                                  "collection_month": qc.valid_month,
                                  "collection_year": qc.valid_year,
                                  "tissue_type": qc.valid_tissue_type,
                                  "tube_number": qc.valid_tube_number,
                                  "new_building": qc.valid_building_code,
                                  "sample_status": qc.valid_sample_status})

        for key, value in c.iteritems():
            try:
                # If there is a validation function, run it and store the result if it succeeds.
                vfunc = validation_funcs[key]
                validated[key] = vfunc(value)
            except e.TsetsedbImportError as exc:
                # Otherwise, store the error msg.
                exceptions[key] = exc.value
            except KeyError:
                try:
                    # If there wasnt a validation function, just copy the value to the new Bunch.
                    validated[key] = c[key]
                except KeyError:
                    raise

        if exceptions:
            self.validation_failures = exceptions
            return validated
        else:
            return validated


class Upload(SurrogatePK, Model):
    __tablename__ = "uploads"

    filename = Column(db.String(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow, unique=True)
    user_id = Column(db.Integer, db.ForeignKey('users.id'))
    validated = Column(db.Boolean, nullable=False, default=False)
    processed = Column(db.DateTime, nullable=True)


class Role(SurrogatePK, Model):
    __tablename__ = 'roles'
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = ReferenceCol('users', nullable=True)
    user = relationship('User', backref='roles')

    def __init__(self, name, **kwargs):
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        return '<Role({name})>'.format(name=self.name)


class User(UserMixin, SurrogatePK, Model):

    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.String(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean, default=False)
    is_admin = Column(db.Boolean, default=False)
    pi_name = Column(db.String(80), nullable=False)
    pi_email = Column(db.String(80), nullable=False)

    uploads = relationship('Upload', backref='user', lazy='dynamic')
    checkout_requests = relationship('CheckoutRequest', backref='user', lazy='dynamic')

    def __init__(self, username, email, pi_name, pi_email, password=None, **kwargs):
        db.Model.__init__(self, username=username, email=email, pi_name=pi_name, pi_email=pi_email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def __repr__(self):
        return '<User({username!r})>'.format(username=self.username)