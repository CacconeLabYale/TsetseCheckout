# -*- coding: utf-8 -*-
import os

from TsetseCheckout import utils

os_env = os.environ


class Config(object):
    SECRET_KEY = os_env['TSETSECHECKOUT_SECRET']  # TODO: Change me
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13
    ASSETS_DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.

    # Host name
    #SERVER_NAME = "0.0.0.0:5000/"

    #

    # Set up Mail stuff
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = utils.get_file_as_string(os_env["TSETSECHECKOUT_M1"]).strip()
    MAIL_PASSWORD = utils.get_file_as_string(os_env["TSETSECHECKOUT_M2"]).strip()
    DEFAULT_MAIL_SENDER = MAIL_USERNAME

    # Set up flask-upload stuff
    UPLOADS_DEFAULT_DEST = "TsetseCheckout/static/uploads/"

    # Admins list
    ADMINS = ['tsetse.sample.db@gmail.com', 'gus.dunn@yale.edu']


class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/example'  # TODO: Change me
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar


class DevConfig(Config):
    """Development configuration."""
    ENV = 'dev'
    DEBUG = True
    DB_NAME = 'dev.db'
    # Put the db file in project root
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)
    SQLALCHEMY_BINDS = {'tsetseDB': 'mysql://root:password@localhost/quickhowto'}
    DEBUG_TB_ENABLED = True
    ASSETS_DEBUG = True  # Don't bundle/minify static assets
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    BCRYPT_LOG_ROUNDS = 1  # For faster tests
    WTF_CSRF_ENABLED = False  # Allows form testing
