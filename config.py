import os


class Config(object):
    # General Config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_default_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///your_database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email Configuration (if needed for alerts/notifications)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']  # List of admin email addresses

    # Monitoring Configuration (add any additional configuration needed for monitoring)
    MONITORING_INTERVAL = 60  # Time in seconds between each server check


class DevelopmentConfig(Config):
    DEBUG = True
    # Development specific configurations can be added here


class TestingConfig(Config):
    TESTING = True
    # Testing specific configurations can be added here


class ProductionConfig(Config):
    # Production specific configurations can be added here
    pass


# You can add more configuration classes if needed