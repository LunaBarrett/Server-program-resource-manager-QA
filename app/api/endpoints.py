from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import ServerResourceUsage

# Create a Blueprint for the API
api = Blueprint('api', __name__)


# Create the get_resource_usage function which retrieves current resources usage data from the server
@api.route('/resource_usage', methods=['GET'])
def get_resource_usage():
    # Retrieve the latest resource usage data from the database
    latest_data = ServerResourceUsage.query.order_by(ServerResourceUsage.timestamp.desc()).first()
    if not latest_data:
        return jsonify({'error': 'No data available'}), 404

    return jsonify({
        'cpu_usage': latest_data.cpu_usage,
        'memory_usage': latest_data.memory_usage,
        'disk_usage': latest_data.disk_usage,
    }), 200


# Create the add_resource_usage function which adds current data to the database
@api.route('/resource_usage', methods=['POST'])
def add_resource_usage():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    resource_usage = ServerResourceUsage(
        cpu_usage=data.get('cpu_usage'),
        memory_usage=data.get('memory_usage'),
        disk_usage=data.get('disk_usage'),
    )

    db.session.add(resource_usage)
    db.session.commit()

    keep_recent_entries()

    return jsonify({'message': 'Resource usage added successfully'}), 201


# Create the keep_recent_entries function, which ensures that the database only stores the 10 most recent entries
def keep_recent_entries():
    # Get the count of all entries
    total_entries = ServerResourceUsage.query.count()

    # If more than ten entries, delete the oldest
    if total_entries > 10:
        # Get the oldest entries that exceed the limit of 10
        excess_entries = ServerResourceUsage.query.order_by(ServerResourceUsage.timestamp.asc()).limit(
            total_entries - 10).all()

        for entry in excess_entries:
            db.session.delete(entry)

        db.session.commit()



