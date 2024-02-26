import asyncio
import logging as log
from asyncua import Client, ua, Server
import requests


import socket

log.basicConfig(format='%(levelname)s: %(message)s', level=log.INFO)

ws_url = f"http://127.0.0.1:5000/"

hostname = socket.gethostname()

ip_address = socket.gethostbyname(hostname)

port = 4840

#r = requests.post('https://httpbin.org/post', data={'key': 'value'})
#r = requests.get('https://api.github.com/events')

class OPCUAClient:
    def __init__(self, ip_address, port):

        self.client = Server()
        

        self.client.set_endpoint(f"opc.tcp://{ip_address}:{port}")
        self.uri = f"http://{ip_address}:{port}"

        print(f"server running at: opc.tcp://{ip_address}:{port}")

        self.stack = []
    
        # set up our own namespace, not really necessary but should as spec
    async def server_init(self):
        await self.client.init()

    async def add_objects(self):
        objects = self.client.get_objects_node()
        self.idx = await self.client.register_namespace(self.uri)

        comm_to_sps_afss = await self.client.nodes.objects.add_object(self.idx, "AFSS_to")
        self.inst_1 = await comm_to_sps_afss.add_variable(self.idx, "inst_1", "")

        await self.inst_1.set_writable(writable=True)


        comm_to_server = await self.client.nodes.objects.add_object(self.idx, "to_server")

        self.afss_ready = await comm_to_server.add_variable(self.idx, "afss_ready", False)
        await self.afss_ready.set_writable(writable=True)

        self.afss_busy = await comm_to_server.add_variable(self.idx, "afss_busy", False)
        await self.afss_busy.set_writable(writable=True)


        self.afss_error = await comm_to_server.add_variable(self.idx, "afss_error", False)
        await self.afss_busy.set_writable(writable=True)


        testing = await self.client.nodes.objects.add_object(self.idx, "testing")
        self.test_busy = await testing.add_variable(self.idx, "test_busy", False)
        await self.test_busy.set_writable(writable=True)

        self.add = await testing.add_variable(self.idx, "add", 0)
        await self.add.set_writable(writable=False)


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
    
    async def work_on_stack(self):
        if not await self.read_variable(self.afss_busy):
            if len(self.stack) > 0:
                log.info(f'self.stack {type(self.stack)}: {self.stack}')
                await self.write_variable(self.inst_1, self.stack[0])
                self.stack.pop(0)


async def main():
    # Replace with your server's IP
    client = OPCUAClient(ip_address, port)
    await client.server_init()
    await client.add_objects()

    try:
        #DONE: cerate nodes, async idk sleep

        current_value = await client.read_variable(client.inst_1)
        print(f"Current value of MyVariable: {current_value}")

        new_value = "inst_to"
        await client.write_variable(client.inst_1, new_value)
        print(f"Updated value of MyVariable: {await client.read_variable(client.inst_1)}")

        async with client.client:
            while True:
                status = await client.read_variable(client.afss_ready)
                log.info(f'status {type(status)}: {status}')
                if status:
                    await client.work_on_stack()
                else:
                    print("AFSS not running")
                log.info(f"status test {await client.read_variable(client.test_busy)}")
                log.info(f"int = {await client.read_variable(client.add)}")
                await client.write_variable(client.add, await client.read_variable(client.add) + 1)
                await asyncio.sleep(1)

    finally:
        pass


if __name__ == "__main__":
    asyncio.run(main(), debug=True)