import psutil
from app.models import ServerResourceUsage
from app import db

def collect_server_resource_usage():
    # Use psutil or another library to collect system metrics
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    # Assume a function to calculate network usage
    network_usage = calculate_network_usage()

    # Create a new ServerResourceUsage object with the collected data
    resource_usage = ServerResourceUsage(
        cpu_usage=cpu_usage,
        memory_usage=memory_usage,
        disk_usage=disk_usage,
        network_usage=network_usage
    )

    # Add the new object to the session and commit it to the database
    db.session.add(resource_usage)
    db.session.commit()

# You may need to schedule this function to run at regular intervals