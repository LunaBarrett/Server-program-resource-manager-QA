import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # General Config
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database', 'userdetails.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email Configuration (if needed for alerts/notifications)
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']  # List of admin email addresses

    # Monitoring Configuration
    MONITORING_INTERVAL = 60  # Time in seconds between each server check


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass


