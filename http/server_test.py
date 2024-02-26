from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from datetime import datetime
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


class MyHandler(BaseHTTPRequestHandler):
        

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.data = [{'message': 'This is a JSON response for GET request'}, {"now": (str(datetime.now()))}, {"now_sec": round(datetime.now().timestamp())}]
        
        json_data = json.dumps(self.data).encode('utf-8')
        self.wfile.write(json_data)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        response = f'This is a different response for POST request. Received data: {post_data.decode("utf-8")}'
        self.wfile.write(response.encode('utf-8'))

def run_server(port=8000):
    server_address = (get_ip_address(), port)
    httpd = HTTPServer(server_address, MyHandler)
    print(f'Starting server on {server_address[0]}:{port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()