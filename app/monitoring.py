import psutil
from app.models import ServerResourceUsage
from app import db, app


def collect_server_resource_usage():
    # Use psutil to collect system metrics
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    # Create a new ServerResourceUsage object with the collected data
    resource_usage = ServerResourceUsage(
        cpu_usage=cpu_usage,
        memory_usage=memory_usage,
        disk_usage=disk_usage,
    )

    # Add the new object to the session and commit it to the database
    db.session.add(resource_usage)
    db.session.commit()
