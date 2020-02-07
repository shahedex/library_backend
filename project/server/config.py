# project/server/config.py

import os

POSTGRES_SERVER_NAME = os.environ.get('POSTGRES_SERVER_NAME')
POSTGRES_USER_NAME = os.environ.get('POSTGRES_USER_NAME')
POSTGRES_USER_PASS = os.environ.get('POSTGRES_USER_PASS')

basedir = os.path.abspath(os.path.dirname(__file__))
postgres_local_base = 'postgresql://' + POSTGRES_USER_NAME +':' + POSTGRES_USER_PASS + '@' + POSTGRES_SERVER_NAME + ':5432/'
database_name = 'library_db'


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'the_$uper_$ecret_key')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name + '_test'
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = 'the_$uper_$ecret_key_f0r_pr0ducti0n'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://' + POSTGRES_USER_NAME +':' + POSTGRES_USER_PASS + '@' + POSTGRES_SERVER_NAME + ':5432/'
