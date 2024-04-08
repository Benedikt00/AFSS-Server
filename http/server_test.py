from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'PUT'])
def handle_requests():
    if request.method == 'GET':
        print("get")
        return 'GET request received'
    
    elif request.method == 'POST':
        data = request.data.decode("utf-8")
        print("post ",  )
        return f'POST request received: {data}'
    
    elif request.method == 'PUT':
        print("put")
        return f'PUT request received + {request.data}'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)