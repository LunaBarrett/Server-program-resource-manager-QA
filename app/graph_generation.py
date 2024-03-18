import matplotlib.pyplot as plt
from app.models import ServerResourceUsage
import os
from app import app

def generate_graphs():
    # Query the last N resource usage records from the database
    data_points = ServerResourceUsage.query.order_by(ServerResourceUsage.timestamp.desc()).limit(100).all()

    # Extract the data for each resource
    timestamps = [data.timestamp for data in data_points]
    cpu_usages = [data.cpu_usage for data in data_points]
    memory_usages = [data.memory_usage for data in data_points]
    disk_usages = [data.disk_usage for data in data_points]
    # ... other resources

    # Generate and save the Memory usage graph
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, memory_usages, label='Memory(RAM) Usage')
    plt.xlabel('Time')
    plt.ylabel('Memory Usage (%)')
    plt.title('Memory(RAM) Usage Over Time')
    plt.legend()
    plt.savefig(os.path.join(app.static_folder, 'images', 'memory_usage.png'))
    plt.close()

    # Generate and save the Disk usage graph
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, disk_usages, label='Disk Usage')
    plt.xlabel('Time')
    plt.ylabel('Disk Usage (%)')
    plt.title('Disk Usage Over Time')
    plt.legend()
    plt.savefig(os.path.join(app.static_folder, 'images', 'disk_usage.png'))
    plt.close()

    # Generate and save the CPU usage graph
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, cpu_usages, label='CPU Usage')
    plt.xlabel('Time')
    plt.ylabel('CPU Usage (%)')
    plt.title('CPU Usage Over Time')
    plt.legend()
    plt.savefig(os.path.join(app.static_folder, 'images', 'cpu_usage.png'))
    plt.close()
