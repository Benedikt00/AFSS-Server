# write_request: {id: "4", jsonrpc: "2.0", method: "PlcProgram.Write", params: {var: "\"web2Plc\".open", value: true}}
#read: {id: "5", jsonrpc: "2.0", method: "PlcProgram.Read", params: {var: "\"web2Plc\".open"}
"""jsonrpc": "2.0", "id": 2, "result":[
{ "name": "Api.Browse" },
{ "name": "Api.Login" },
{ "name": "Api.Logout" },
{ "name": "Api.GetPermissions" },
{ "name": "PlcProgram.Read" },
{ "name": "PlcProgram.Write" }
Api.Ping
]"""



from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/jsonrpc', methods=['POST'])
def handle_jsonrpc():
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Process the JSON-RPC request (example implementation)
        if data['jsonrpc'] != '2.0':
            raise ValueError('Invalid JSON-RPC version')

        method = data['method']
        if params in data.keys():
            params = data.get('params', {})
        id = data.get('id')

        # Example method handling
        if method == 'echo':
            result = params  # Echo back the parameters as result
        
        elif method == 'Api.Login':
            result = {"token": "46290"}
        
        elif method == "PlcProgram.Read":
            result = 501

        elif method == "PlcProgram.Write":
            result = {"sucsess": ""}

        elif method == "Api.Ping":
            return "200"
        
        else:
            raise ValueError('Method not found')

        # Create the JSON-RPC response
        response = {
            'jsonrpc': '2.0',
            'result': result,
            'id': id
        }
    except Exception as e:
        # Create an error response in case of any exceptions
        response = {
            'jsonrpc': '2.0',
            'error': {
                'code': -32600,
                'message': str(e)
            },
            'id': data.get('id') if 'id' in data else None
        }

    # Return the JSON response
    return jsonify(response)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5001, debug=True)



