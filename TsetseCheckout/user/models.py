# -*- coding: utf-8 -*-
import datetime as dt

from bunch import Bunch
from flask import g
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


class CheckoutRequest(SurrogatePK, Model):
    __tablename__ = "checkout_requests"

    username = Column(db.Integer, db.ForeignKey('users.id'))
    to_produce = Column(db.String(60), nullable=False)  # TODO: add validation
    village_symbol = Column(db.String(15), nullable=False)  # TODO: add validation
    collection_month = Column(db.Integer(), nullable=False)  # TODO: add validation
    collection_year = Column(db.Integer(), nullable=False)  # TODO: add validation
    sample_type = Column(db.String(15), nullable=False)  # TODO: add validation
    tube_number = Column(db.Integer, nullable=False)  # TODO: add validation
    date_of_request = Column(db.DateTime, nullable=False)
    date_approved = Column(db.DateTime, nullable=True)
    new_building = Column(db.String(5), nullable=False)  # TODO: add validation
    new_room = Column(db.Integer, nullable=False)
    new_cryo = Column(db.String(30), nullable=False)
    sample_status = Column(db.String(15), nullable=False)  # TODO: add validation
    passed_validation = Column(db.Boolean, nullable=True)

    def __init__(self, username, to_produce, village_symbol, collection_month, collection_year, sample_type,
                 tube_number, date_of_request, date_approved, new_building, new_room, new_cryo, sample_status,
                 passed_validation, **kwargs):
        columns = Bunch(username=username, to_produce=to_produce, village_symbol=village_symbol,
                        collection_month=collection_month, collection_year=collection_year, sample_type=sample_type,
                        tube_number=tube_number, date_of_request=date_of_request, date_approved=date_approved,
                        new_building=new_building, new_room=new_room, new_cryo=new_cryo, sample_status=sample_status,
                        passed_validation=passed_validation)
        self._validate_columns(columns)
        db.Model.__init__(*columns, **kwargs)


class Upload(SurrogatePK, Model):
    __tablename__ = "uploads"

    filename = Column(db.String(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow, unique=True)
    user_id = Column(db.Integer, db.ForeignKey('users.id'))
    processed = Column(db.DateTime, nullable=True)

    # def __init__(self, filename, user_id, **kwargs):
    #     db.Model.__init__(self, filename=filename, user_id=user_id, **kwargs)


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