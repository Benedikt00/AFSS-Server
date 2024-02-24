import asyncio
import logging
from asyncua import Client, ua, Server

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

import socket

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

hostname = socket.gethostname()

ip_address = socket.gethostbyname(hostname)

port = 4840

class OPCUAClient:
    def __init__(self, server_url):
        self.server_url = server_url
        self.client = Server()
        self.client.init()

        self.client.set_endpoint(f"opc.tcp://{ip_address}:{port}")
        uri = f"http://{ip_address}:{port}"
    
        # set up our own namespace, not really necessary but should as spec
        idx = self.client.register_namespace(uri)

    


    async def read_variable(self, variable_node):
        value = await variable_node.get_value()
        return value

    async def write_variable(self, variable_node, value):
        await variable_node.set_value(value)

    async def get_available_slots(self):
        server_method = await self.client.get_node(ua.NodeId("ServerMethod", 2))  # Replace with your method NodeId
        result = await server_method.call_method(ua.Variant(0, ua.VariantType.Int64))
        return result

    async def display_values(self, values):
        for value in values:
            print(f"Displaying value: {value}")
            await asyncio.sleep(2)  # Display each value for 2 seconds


async def main():
    server_url = f"opc.tcp://{ip_address}:{port}"  # Replace with your server's IP
    client = OPCUAClient(server_url)
    
    try:
        #TODO: cerate nodes, async idk sleep
        # Example of reading and writing variables
        my_variable_node = await client.get_node("ns=2;s=MyObject.MyVariable")
        current_value = await client.read_variable(my_variable_node)
        print(f"Current value of MyVariable: {current_value}")

        new_value = 42.0
        await client.write_variable(my_variable_node, new_value)
        print(f"Updated value of MyVariable: {await client.read_variable(my_variable_node)}")

        # Example of getting available slots
        available_slots = await client.get_available_slots()
        print(f"Available slots: {available_slots}")

        # Example of displaying values
        values_to_display = [10, 20, 30]
        await client.display_values(values_to_display)

    finally:
        pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main(), debug=True)