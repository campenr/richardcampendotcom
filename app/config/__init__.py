"""
campen.co has two different configuration environments:
 - dev
 - production

Each configuration environment has different configuration settings. This is achieved by using flask's
`app.config_from_object` and importing one of the two different configuration objects below, that represent the two
different environments. To run the application under the different environments run using the matching uwsgi
configuration file, which specifies the configuration to load as an environment variable.

"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    Base application configuration object.

    Any items in this class that are set as None or '' must be implemented by subclasses. All other configuration
    options are constant cross environment and should not be overwritten.

    Things to pay particular attention to are:
        - The secret key
        - The SQL Database URI and username/password
        - The redis server URI and username/password

    """

    DEBUG = False
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = ''
    # The migrate repo is constant across environments as they are deployed in separate folders already
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """
    Development environment configuration.

    """

    # general
    app_name = 'campenco'

    # SQL
    psql_password = 'password'
    psql_port = '5432'
    psql_db = app_name
    SQLALCHEMY_DATABASE_URI = "postgresql://%s:%s@localhost:%s/%s" % (app_name, psql_password, psql_port, psql_db)

    # redis
    redis_password = ''
    redis_port = '6379'
    redis_db = '0'
    REDIS_URI = 'redis://localhost:%s/%s' % (redis_port, redis_db)

    # celery
    CELERY_BROKER_URL = REDIS_URI
    CELERY_RESULT_BACKEND = REDIS_URI


class ProductionConfig(Config):
    """
    Production environment configuration.

    """

    # general
    app_name = 'campenco'

    # SQL
    psql_password = 'd2TqRDLN7fwdJ5OLQyKHew43Y'
    psql_port = '5432'
    psql_db = app_name
    SQLALCHEMY_DATABASE_URI = "postgresql://%s:%s@localhost:%s/%s" % (app_name, psql_password, psql_port, psql_db)

    # redis
    redis_password = ''
    redis_port = '6379'
    redis_db = '1'
    REDIS_URI = 'redis://localhost:%s/%s' % (redis_port, redis_db)

    # celery
    CELERY_BROKER_URL = REDIS_URI
    CELERY_RESULT_BACKEND = REDIS_URI


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}