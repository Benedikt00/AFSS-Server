from opcua import Client
import time
import datetime


def opcua
    # Replace this with the actual endpoint of your Raspberry Pi OPC UA server
    server_endpoint = "opc.tcp://192.168.0.46:4841"

    try:
        # Create a client and connect to the server
        client = Client(server_endpoint)
        client.connect()



        # Specify the Node IDs for the Temperature and Windspeed variables under the Station node
        temperature_node_id = client.get_node("ns=2;i=2")
        windspeed_node_id = client.get_node("ns=2;i=3")
        req_nod_id = client.get_node("ns=2;i=4")
        time_node = client.get_node("ns=2;i=5")
        change_node = client.get_node("ns=2;i=6")

        start = True
        i = 0
        while True:

            time_rsp = client.get_node(time_node).get_value()
            state = client.get_node(change_node).get_value()

            if state == "True":
                response = "False"
            else:
                response = "True"
            now = datetime.datetime.now()
            client.set_values([change_node], [response])

            time_after_set_rsp = client.get_node(time_node).get_value()

            while time_rsp == time_after_set_rsp:
                time_after_set_rsp = client.get_node(time_node).get_value()

            if i > 0:
                #print(now)
                #print(time_after_set_rsp)
                diff = now-time_after_set_rsp
                print(f"Timediff: {diff.total_seconds() * 1000} ms")

            i += 1
            if i > 10:
                break
            # Read the values of Temperature and Windspeed variables
            #temperature_value = client.get_node(temperature_node_id).get_value()
            #windspeed_value = client.get_node(windspeed_node_id).get_value()
            #if start:
            #    start = False
            #else:
            #    start = True

            #client.set_values([req_nod_id], [start])

            #print(f"Temperature: {temperature_value} °C")
            #print(f"Windspeed: {windspeed_value} m/s")

            #time.sleep(5)



    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Disconnect from the server
        client.disconnect()

if __name__ == "__main__":
    opcua_client()