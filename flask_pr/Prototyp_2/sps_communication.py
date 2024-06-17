import requests
import json
from internal_logging import *
class sps_com():
    def __init__(self, ip_address):
        self.ip_address = ip_address

        self.session_token = 0
        self.session_id = 1
        self.url = ip_address + "/api/jsonrpc"

        self.com_db = "\"http_com\""
    
    def new_ip_address(self, ip):
        self.url = ip + "/api/jsonrpc"
        self.ip_address = ip

    def connect_to_sps(self, username, password):
        logcb(f"opiosetg {self.url}")
        headers = {
            'Content-Type': 'application/json'
        }

        data = {
            "id": str(self.session_id),
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
            logcb(f"Connected to {self.ip_address}: {req}")
            if "error" in req.keys():
                return req["error"]["message"]
            token = req["result"]["token"]
            self.session_token = token
            self.session_id += 1
            return "OK: 200"

        except requests.exceptions.HTTPError as http_err:
            logcr(f"HTTP error occurred: {http_err}")
            return http_err
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
    
    def ses_id(self):
        self.session_id += 1
        return str(self.session_id - 1)

    def enable_testmode(self):
        return self.write_variable("DEBUG_MODE", True)

    def ping_sps(self):
        data = {"jsonrpc":"2.0", "method":"Api.Ping", "id": self.ses_id()}
        self.send_data_to_sps(data)


    def write_variable(self, var_name, value):
        data = {"id": self.ses_id(), "jsonrpc": "2.0", "method": "PlcProgram.Write", "params": {"var": f"{self.com_db}.{var_name}", "value": str(value)}}
        req = self.send_data_to_sps(data)
        return req
    
    def read_variable(self, var_name):
        pass

    def write_multiple_variables(self, var_dict):
        das = []
        
        for key, val in var_dict.items():
            das.append({"id": self.ses_id(), "jsonrpc": "2.0", "method": "PlcProgram.Write", "params": {"var": f"{self.com_db}.{key}", "value": str(val)}})
        
        req = self.send_data_to_sps(das)