import requests
import socket

def get_ip_address():
    try:
        # Get the hostname of the local machine
        hostname = socket.gethostname()

        # Get the IP address associated with the hostname
        ip_address = socket.gethostbyname(hostname)

        return ip_address
    except Exception as e:
        print(f"Error getting IP address: {e}")
        return None

# Replace 'http://localhost:8000' with the actual URL of your server
server_url = f'http://{get_ip_address()}:8000'

try:
    # Testing a GET request
    response_get = requests.get(server_url)
    print(f"GET Response: {response_get.text}")

    # Testing a POST request
    data = {'key': 'value'}
    response_post = requests.post(server_url, json=data)
    print(f"POST Response: {response_post.text}")
except requests.ConnectionError:
    print("Failed to connect to the server. Make sure the server is running.")
except Exception as e:
    print(f"Error: {e}")