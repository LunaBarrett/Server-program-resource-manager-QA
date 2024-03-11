from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import ServerResourceUsage

api = Blueprint('api', __name__)


@api.route('/resource_usage', methods=['POST'])
def add_resource_usage():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Assume data contains the necessary server resource usage information
    resource_usage = ServerResourceUsage(
        cpu_usage=data.get('cpu_usage'),
        memory_usage=data.get('memory_usage'),
        disk_usage=data.get('disk_usage'),
        network_usage=data.get('network_usage')
    )

    db.session.add(resource_usage)
    db.session.commit()
    return jsonify({'message': 'Resource usage added successfully'}), 201


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
        'network_usage': latest_data.network_usage
    }), 200

# You can add more API endpoints as needed