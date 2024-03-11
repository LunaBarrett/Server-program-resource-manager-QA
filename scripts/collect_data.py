import requests
import psutil

# Replace with the actual URL of your Flask application's API endpoint
API_ENDPOINT = 'http://localhost:5000/api/resource_usage'

def collect_and_send_data():
    # Collect server resource usage data
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    # Assume a function to calculate network usage
    network_usage = calculate_network_usage()

    # Prepare the data payload
    data = {
        'cpu_usage': cpu_usage,
        'memory_usage': memory_usage,
        'disk_usage': disk_usage,
        'network_usage': network_usage
    }

    # Send a POST request to the Flask application's API endpoint
    response = requests.post(API_ENDPOINT, json=data)
    if response.status_code == 201:
        print('Data sent successfully')
    else:
        print('Failed to send data', response.content)

def calculate_network_usage():
    # Implement logic to calculate network usage
    # This is just a placeholder function
    return 0

if __name__ == '__main__':
    collect_and_send_data()