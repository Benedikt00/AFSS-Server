import requests
import json
from internal_logging import *
class sps_com():
    def __init__(self, ip_address):
        self.ip_address = ip_address

        self.session_token = 0

        self.url = ip_address + "/api/jsonrpc"

    def connect_to_sps(self, username, password):
        headers = {
            'Content-Type': 'application/json'
        }

        data = {
            "id": "1",
            "jsonrpc": "2.0",
            "method": "Api.Login",
            "params": {
                "user": username,
                "password": password,
            }
        }
        try:
            response = requests.post(self.url, data=json.dumps(data), headers=headers, verify=False)
            response.raise_for_status()  # Raise an exception for HTTP errors
            req = json.loads(response.content.decode('utf-8'))
            token = req["result"]["token"]
            self.session_token = token
            return "OK: 200"

        except requests.exceptions.HTTPError as http_err:
            logcr(f"HTTP error occurred: {http_err}")
            return err
        except Exception as err:
            logcr(f"Other error occurred: {err}")
            return err

    def send_data_to_sps(self, data: dict):
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-Token': str(self.session_token)
        }
        response = requests.post(self.url, data=json.dumps(data), headers=headers, verify=False)
        response.raise_for_status()  # Raise an exception for HTTP errors
        req = json.loads(response.content.decode('utf-8'))

        return req

    def ping_sps(self):
        data = {"jsonrpc":"2.0", "method":"Api.Ping", "id":1}
        self.send_data_to_sps(data)

    def write_variable(self, var_name, value):
        return "501"
    
    def read_variable(self, var_name):
        pass