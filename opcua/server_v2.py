from opcua import Server
import mysql.connector
import re

pattern = r"'([A-Za-z0-9]+)'"



# Replace these values with your MySQL database connection details
db_host = 'localhost'  # Assuming the database is on the same machine
db_user = 'root'
db_password = '112358'
db_database = 'test_db_bauteile'

# Function to query the database and get the position of a part
def get_position_by_name(part_name):
    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_database
        )

        cursor = connection.cursor()
        query = f"SELECT posi FROM bauteile WHERE name = '{part_name}';"
        print(f"query: {query}")
        cursor.execute(query)
        #position = cursor.fetchone()[0] if cursor.rowcount > 0 else None
        for x in cursor.fetchall():
            match = re.search(pattern, str(x))
            return match.group(1)

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return None

    finally:
        pass
        #if connection.is_connected():
        #    connection.close()

# Create an OPC UA server
server = Server()
server.set_endpoint("opc.tcp://192.168.0.19:4840")

# Setup the server namespace
uri = "http://192.168.0.19:4840"
idx = server.register_namespace(uri)

# Create a new Object node
obj = server.nodes.objects.add_object(idx, "MyObject")

# Create a new variable node for position
var = obj.add_variable(idx, "Position", "")
var.set_writable()

# Start the server
server.start()
print("OPC UA server started")

# Server loop
try:
    while True:
        part_name = input("Enter the part name to get its position (or 'exit' to stop): ")
        if part_name.lower() == 'exit':
            break

        position = get_position_by_name(part_name)
        if position is not None:
            var.set_value(position)
            print(f"Position for {part_name}: {position}")
        else:
            print(f"No position found for {part_name}")

finally:
    # Stop the server on program exit
    server.stop()
    print("OPC UA server stopped")