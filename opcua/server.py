import opcua
from opcua import Server, ua
import random
import time

#import mysql.connector
#
#mydb = mysql.connector.connect(
#  host="localhost",
#  username="root",
#  password="112358",
#  database="test_db_bauteile"
#)
#
#mycursor = mydb.cursor()
#
#mycursor.execute("SELECT * FROM bauteile")
#
#db = mycursor
#
#dbs = []
#
#for x in db:
#    dbs.append(x)

#print(dbs)

s = opcua.Server()
s.set_server_name("OpcUa Test Server")
s.set_endpoint("opc.tcp://192.168.0.19:4841")

# Register the OPC UA namespace
idx = s.register_namespace("http://192.168.0.19:4841")
# start the OPC UA server (no tags at this point)
s.start()

objects = s.get_objects_node()
# Define a Weather Station object with some tags
myobject = objects.add_object(idx, "Station")
db_bauteile = objects.add_object(idx, "Database")

#inhalt = db_bauteile.add_variable(idx, "Inhalt", list(dbs))
#inhalt.set_writable(writable=True)

# Add a Temperature tag with a value and range
myvar1 = myobject.add_variable(idx, "Temperature", 25)
myvar1.set_writable(writable=True)

# Add a Windspeed tag with a value and range
myvar2 = myobject.add_variable(idx, "Windspeed", 11,4,4)
myvar2.set_writable(writable=True)

# Cycle every 5 seconds with simulated data
while True:
    myvar1.set_value(random.randrange(25, 29))
    myvar2.set_value(random.randrange(10, 20))
    time.sleep(5)