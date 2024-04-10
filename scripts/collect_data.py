import requests
import psutil

# Sets the api endpoint for the flask application to use
API_ENDPOINT = 'http://localhost:5000/api/resource_usage'


def collect_and_send_data():
    # Collect server resource usage data
    cpu_usage = psutil.cpu_percent(interval=1.0)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    # Prepare the data payload
    data = {
        'cpu_usage': cpu_usage,
        'memory_usage': memory_usage,
        'disk_usage': disk_usage,
    }

    # Send a POST request to the Flask application's API endpoint
    response = requests.post(API_ENDPOINT, json=data)
    if response.status_code == 201:
        print('Data sent successfully')
    else:
        print('Failed to send data', response.content)


if __name__ == '__main__':
    collect_and_send_data()
