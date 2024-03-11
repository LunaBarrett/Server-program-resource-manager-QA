from flask import Blueprint

# Create a Blueprint for the API
api = Blueprint('api', __name__)

# Import the endpoints module to associate the routes with the Blueprint
from . import endpoints

