from opcua import Client

def create_new_node():
    # Replace this with the actual endpoint of your OPC UA server
    server_endpoint = "opc.tcp://admin@192.168.0.19:4841"



    try:
        # Create a client and connect to the server
        client = Client(server_endpoint)
        client.connect()

        # Get the root folder (objects) node
        root = client.get_root_node()

        # Specify the namespace index for your server
        idx = client.get_namespace_index("http://192.168.0.19:4841")

        # Create a new node under the root with a variable called "NewVariable"
        objects = client.get_objects_node()
        new_node = objects.add_object(idx, "NewVariable2")

        # Add a variable to the new node
        new_variable = new_node.add_variable(idx, "Value", 2)
        new_variable.set_writable()

        print("New node 'NewVariable' created successfully.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Disconnect from the server
        client.disconnect()

if __name__ == "__main__":
    create_new_node()