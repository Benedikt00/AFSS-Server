import requests
import json
import certifi

def send_post_request(url, data):
	headers = {
		'Content-Type': 'application/json'
	}

	try:
		response = requests.post(url, data=json.dumps(data), headers=headers, verify=False)
		response.raise_for_status()  # Raise an exception for HTTP errors
		print(f"Response Status Code: {response.status_code}")
		req = json.loads(response.content.decode('utf-8'))
		print(f"Response Content: {req}")
		token = req["result"]["token"]

		return token
	except requests.exceptions.HTTPError as http_err:
		print(f"HTTP error occurred: {http_err}")
	except Exception as err:
		print(f"Other error occurred: {err}")

def send_post_request_secure(url, data, token):
	headers = {
		'Content-Type': 'application/json',
		'X-Auth-Token': str(token)
	}
	try:
		response = requests.post(url, data=json.dumps(data), headers=headers, verify=False)
		response.raise_for_status()  # Raise an exception for HTTP errors
		print(f"Response Status Code: {response.status_code}")
		req = response.content.decode('utf-8')
		print(f"Response Content: {req}")

	except requests.exceptions.HTTPError as http_err:
		print(f"HTTP error occurred: {http_err}")
	except Exception as err:
		print(f"Other error occurred: {err}")


if __name__ == "__main__":
	url = "https://10.130.110.195/api/jsonrpc"  # Replace with your URL
	data = {
		"id": "1",
		"jsonrpc": "2.0",
		"method": "Api.Login",
		"params": {
			"user": "stick",
			"password": "stick"
		}
	}

	tok = send_post_request(url, data)
	print(tok, " Token")
	dt = [{
		"jsonrpc": "2.0",
		"method": "PlcProgram.Write",
		"id": 1,
		"params": {
			"var": "\"lol\"", "value": 69
		}
	}]
	print(dt)
	
	send_post_request_secure(url, dt, tok)