from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_apscheduler import APScheduler
from config import Config
from app.api.endpoints import api as api_blueprint
from scripts.collect_data import collect_and_send_data
from app.extensions import db, migrate



# Initialize the Flask application
app = Flask(__name__)

# Load the configuration from the config.py file
app.config.from_object(Config)

# Initialize SQLAlchemy with the Flask app
#db = SQLAlchemy(app)

# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)

# Initialize APScheduler
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


# Schedule the data collection function to run every X minutes
@scheduler.task('interval', id='do_collect_data', seconds=10, misfire_grace_time=900)
def job():
    collect_and_send_data()


# Initialize Flask-Migrate for database migrations
#migrate = Migrate(app, db)

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Specify the login view


# Register the blueprint
from app.api.endpoints import api as api_blueprint
app.register_blueprint(api_blueprint, url_prefix='/api')


# Import models and views
from app import models, views


# User loader callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

# You can add any other initialization code here

