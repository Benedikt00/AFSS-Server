from config import Config
from extensions import db
from models import *

import logging as log
from internal_logging import *


class instruction_stack_afss():
    def __init__(self):
        self.max_preload_length = 5
        self.preload = 0

        self.areas = Config.AFSS_AREAS
        self.num_storage = len(self.areas)

        self.order_id = 0
        self.instruction_num = 1

        self.done_instructions = [0]
        self.pending_instructions = []
        self.interrupts_in_system = []

        self.fb = "TB"
        self.shifter_coeff = 10 # um den förderbandschieber vom schrank zu differenzieren ist der schieber des schrankes x das gerät x+10
        self.shifters = Config.AFSS_SHIFTER_POSITIONS
        self.shifter_clearance = - 250

        self.real_state = {}
        

    def create_stack(self):
        self.stack = {self.fb: []}
        for area in self.areas.keys():
            self.stack[area] = []
        
        for area in self.areas.keys():
            self.stack[str(int(area) + self.shifter_coeff)] = []


    def get_max_value_in_stack(self, key = None):
        max_value = None
        if not key:
            for area in self.stack.items():
                for inst in area:
                    id = inst["id"]
                    max_value = max(id, max_value)
        
        if key: 
            for inst in self.stack[key]:
                    id = inst["id"]
                    max_value = max(id, max_value)
                            
        return max_value


    def on_stack_empty(self):
        self.instruction_num = 1
        self.done_instructions = [0]
        pass


    def show_stack(self):
        strang = ""
        for x in self.stack.keys():
            strang += f"{x}: {self.stack[x]}\n"

        return strang


    def is_location_in_afss(self, location):
        return str(location)  in self.areas.keys()


    def create_order(self, order: list, *, interrupt = False):
        """Inserts the commants into the stack
        
        Keyword arguments:
        order -- commands
        interrupt -- if true, the order is put on priority list
        Return: return_description
        """
        
        logcb(f"Order: {order}")

        order_id = self.order_id

        for i, instruction in enumerate(order):

            if not interrupt:
            
                if "MOV" in instruction.keys():
                    mv_inst = instruction["MOV"]
                    area = mv_inst["area"]
                    rel: list = mv_inst["rel"] 
                    pos = mv_inst["pos"]

                    abs_relations = []

                    for x in rel:
                        if x == 0:
                            abs_relations.append(0)
                        else:
                            abs_relations.append(x + self.instruction_num)

                    new_ift = {"instruction_id": self.instruction_num, 
                                "order_id": order_id, 
                                "relation": abs_relations, 
                                "instruction": {"area": area, "pos": pos}}
                    
                    self.stack[str(area)].append(new_ift)

            if interrupt:
                if "MOV" in instruction.keys():

                    mv_inst = instruction["MOV"]
                    area = mv_inst["area"]
                    rel: list = mv_inst["rel"] 
                    pos = mv_inst["pos"]

                    abs_relations = []

                    for x in rel:
                        if x == 0:
                            abs_relations.append(0)
                        else:
                            abs_relations.append(x + self.instruction_num)

                    new_ift = {"instruction_id": self.instruction_num, 
                                "order_id": order_id, 
                                "relation": abs_relations, 
                                "instruction": {"area": area, "pos": pos}}
                    
                    self.stack[str(area)].append(new_ift)

                if "BR" in instruction.keys():
                    self.stack["0"].append({"instruction_id": self.instruction_num, 
                                            "order_id": order_id, 
                                            "relation": 0,
                                            "instruction": {"area": 0, "pos": "prep_br" }})

            self.instruction_num += 1

        self.order_id += 1


    def get_FX0_for_area(self, area):
        FX0 = db.session.query(Location).filter_by(area=area, category = "SF").first()
        if not FX0:
            raise Exception(f"No FX0 found for area: {area}")
        return FX0.position


    def get_current_orders(self):
        current_orders = []
        for instruction in self.pending_instructions:
            if instruction['order_id'] not in current_orders:
                current_orders.append(instruction['order_id'])
        
        return current_orders 


    def pos_z_zero(pos):
        pos["z"] == 0
        return pos


    def generate_path(self, start_location, end_location): #box moving operation

        start_location = Location.query.get_or_404(start_location)
        end_location = Location.query.get_or_404(end_location)

        start_area = start_location.area
        end_area = end_location.area

        start_area_s = str(start_area)
        end_area_s = str(end_area)
        
        if ((not self.is_location_in_afss(start_area)) or (not self.is_location_in_afss(end_area))):
            return False # not a afss job
        
        if start_area == end_area: #an area intern job
            start_xyz = start_location.position 

            end_xyz = end_location.position

            inst = [{"MOV": {"area": start_area, "pos": start_xyz, "dir": 1, "rel": [0]}}, 
                    {"MOV": {"area": start_area, "pos": end_xyz, "dir": -1, "rel": [-1]}}]

        f_diff = self.areas[end_area_s] - self.areas[start_area_s]

        if start_area != 0: #starts in afss area
            start_xyz = start_location.position

            if end_area == 0: # afss to L0
                end_xyz = 0
                                                                    #dir: 1 für aufladen, -1 für abladen
                inst = [{"MOV": {"area": start_area, "pos": start_xyz, "dir": 1, "rel": [0]}}, 
                        {"MOV": {"area": start_area + self.shifter_coeff, "pos": 0, "rel": [0]}}, #self.shifters[start_area]
                        
                        {"MOV": {"area": start_area, "pos": self.get_FX0_for_area(start_area), "dir": -1, "rel": [-1, -2]}},

                        {"MOV": {"area": self.fb, "pos": self.shifter_clearance, "rel": [-1]}},

                        {"MOV": {"area": start_area + self.shifter_coeff, "pos": self.shifters[start_area_s], "rel": [-1]}},

                        {"MOV": {"area": self.fb, "pos": f_diff - self.shifter_clearance, "rel": [-2]}}]
                
                
            else: # afss to afss
                end_xyz = end_location.position
                inst = [

                    {"MOV": {"area": start_area, "pos": start_xyz, "dir": 1, "rel": [0]}}, 
                    {"MOV": {"area": start_area + self.shifter_coeff, "pos": 0, "rel": [0]}},
                    {"MOV": {"area": end_area, "pos": self.pos_z_zero(self.get_FX0_for_area(end_area)), "dir": 1, "rel": [-1]}},

                    {"MOV": {"area": start_area, "pos": self.get_FX0_for_area(start_area), "dir": -1, "rel": [-1, -2]}},
                    
                    {"MOV": {"area": start_area + self.shifter_coeff, "pos": self.shifters[start_area_s], "rel": [-1]}},

                    {"MOV": {"area": self.fb, "pos": self.shifter_clearance, "rel": [-1]}},

                    {"MOV": {"area": start_area + self.shifter_coeff, "pos": 0, "rel": [-1]}},

                    {"MOV": {"area": self.fb, "pos": f_diff - self.shifter_clearance, "rel": [-1]}},
                    {"MOV": {"area": end_area + self.shifter_coeff, "pos": self.shifters[end_area_s], "rel": [-2]}}, #self.shifters[start_area]

                    {"MOV": {"area": self.fb, "pos": self.shifter_clearance, "rel": [-1, -2]}},

                    {"MOV": {"area": end_area + self.shifter_coeff, "pos": 0, "rel": [-1]}}, #self.shifters[start_area]

                    {"MOV": {"area": end_area, "pos": self.get_FX0_for_area(end_area), "dir": 1, "rel": [-1]}},
                    {"MOV": {"area": end_area, "pos": end_xyz, "dir": 1, "rel": [-1]}}
                    ]

        elif start_area == 0: #ends in afss area

            start_xyz = 0

            if end_area != 0: # L0 to afss
                end_xyz = end_location.position

                inst = [
                        {"MOV": {"area": end_area, "pos": self.pos_z_zero(self.get_FX0_for_area(start_area)), "dir": 1, "rel": [0]}},
                        {"MOV": {"area": self.fb, "pos": f_diff - self.shifter_clearance, "rel": [0]}},
                        {"MOV": {"area": end_area + self.shifter_coeff, "pos": self.shifters[start_area_s], "rel": [0]}},
                        
                        {"MOV": {"area": self.fb, "pos": self.shifter_clearance, "rel": [-1, -2]}},

                        {"MOV": {"area": end_area + self.shifter_coeff, "pos": 0, "rel": [-1]}}, #self.shifters[start_area]

                        {"MOV": {"area": end_area, "pos": self.get_FX0_for_area(end_area), "dir": 1, "rel": [-1]}},

                        {"MOV": {"area": end_area, "pos": end_xyz, "dir": 1, "rel": [-1]}}
                        
                        ]
                
        return inst


    def request_box_return(self):
        instruction = [{"BR": {}}]
        order = self.create_order(instruction)#TODO: ?
        self.create_order(order, interrupt=True)


    def insert_storing_operation(self, start_location, end_location):
        path = self.generate_path(start_location, end_location)
        self.create_order(path, interrupt=True)

    def norm_storing_operation(self, start_location, end_location):
        logcb(f"op: {start_location} -> {end_location}")
        path = self.generate_path(start_location, end_location)

        self.create_order(path)



    def has_lower_order_id(self, given_order_id):
        for key, instructions in self.stack.items():
            for instruction in instructions:
                if instruction['order_id'] < given_order_id:
                    return True
        return False


    def get_lowest_order_id(self):
        lowest_order_id = float('inf')

        for key, instructions in self.stack.items():
            for instruction in instructions:
                if instruction['order_id'] < lowest_order_id:
                    lowest_order_id = instruction['order_id']

        return lowest_order_id


    def has_order_id(self, order_id):
        for key, instructions in self.stack.items():
            for instruction in instructions:
                if instruction['order_id'] == order_id:
                    return True
        return False


    def get_and_delete_instruction(self, instruction_id):
        for key, instructions in self.stack.items():
            for i, instruction in enumerate(instructions):
                if instruction['instruction_id'] == instruction_id:
                    # Remove the instruction from the list
                    removed_instruction = instructions.pop(i)
                    return removed_instruction
        return None  # If the instruction_id is not found


    def is_lowest_instruction(self, given_instruction, data_dict):
        lowest_instruction = None
        try:
            for instruction in data_dict:
                if lowest_instruction is None or \
                instruction['order_id'] < lowest_instruction['order_id'] or \
                (instruction['order_id'] == lowest_instruction['order_id'] and instruction['instruction_id'] < lowest_instruction['instruction_id']):
                    lowest_instruction = instruction
        except Exception as e:
            logcb(f"Error: \n gi: {given_instruction},\n dd: {data_dict}")
            logcr(e)
        return given_instruction == lowest_instruction


    def get_current_bmos(self, executed_inst_id: int):
        
        executed_inst_id = int(executed_inst_id)
        instructions_to_send = []

        logcc(f"----- id = {executed_inst_id} --------\n")

        interrupt_in_system = (self.interrupts_in_system != [])

        logcb(f"interrupts: {self.interrupts_in_system}, {interrupt_in_system}")
        logcb(f"pending: {self.pending_instructions}")
        logcb(f"done: {self.done_instructions}\n\n")

        self.pending_instruction_ids = [instruction['instruction_id'] for instruction in self.pending_instructions]

        if (executed_inst_id not in self.pending_instruction_ids) and (executed_inst_id != 0): #
            logcb(f"No instruction pending with id: {executed_inst_id}")
            return []

        if executed_inst_id != 0: #get the next instruciton
            
            executed_inst = self.get_and_delete_instruction(executed_inst_id)
            last_order_id = executed_inst["order_id"]
            self.done_instructions.append(executed_inst_id)

            self.pending_instructions.remove(executed_inst)
            
            # remove the instruction from stack
            for area, instructions in self.stack.items():
                for instruction in instructions:
                    if instruction["instruction_id"] == executed_inst_id:
                        instructions.remove(instruction)
                        break
            
            if interrupt_in_system: #complete current order
                for area, instructions in self.stack.items():
                    for instruction in instructions:

                        if instruction["order_id"] in self.get_current_orders(): #do not let any new orders in the system

                            for relation in instruction["relation"]:
                                if relation in self.done_instructions:

                                    if instruction["instruction_id"] not in self.pending_instruction_ids:
                                        instructions_to_send.append(instruction)
                    
                if instructions_to_send == []: #no more orders to complete, let's begin the interrupt

                    next_order = min(self.interrupts_in_system)

                    for area, instructions in self.stack.items():
                        for instruction in instructions:
                            if instruction["order_id"] == next_order: #do not let any other orders in the system

                                for relation in instruction["relation"]:
                                    if relation in self.done_instructions:

                                        if instruction["instruction_id"] not in self.pending_instruction_ids:
                                            instructions_to_send.append(instruction)
            
            if not interrupt_in_system: #random bullshit go
                for area, instructions in self.stack.items():
                    for instruction in instructions:

                        for relation in instruction["relation"]:
                            if relation in self.done_instructions:

                                if instruction["instruction_id"] not in self.pending_instruction_ids:
                                    instructions_to_send.append(instruction)
                            
                            if relation == 0:
                                if self.is_lowest_instruction(instruction, instructions) and instruction["instruction_id"] not in self.pending_instruction_ids:
                                    instructions_to_send.append(instruction)

        if executed_inst_id == 0: # sps has no clue

            if self.pending_instructions != []: #sps has forgotten pending instructions

                for instruction in self.pending_instructions:
                    instructions_to_send.append(instruction)
            
            if self.pending_instructions == []: #no pending insts, random bullshit go
                for area, instructions in self.stack.items():
                    for instruction in instructions:

                        for relation in instruction["relation"]:
                            if relation in self.done_instructions:
                                
                                instructions_to_send.append(instruction)
                            
                            if relation == 0:
                                if self.is_lowest_instruction(instruction, instructions) and instruction["instruction_id"] not in self.pending_instruction_ids:
                                    instructions_to_send.append(instruction)
        

        for x in instructions_to_send:
            if x != 0: #cant have that, otherwise the paralellity will break
                self.pending_instructions.append(x)
            

        return instructions_to_send



if __name__ == '__main__':
    stack = instruction_stack_afss()

    stack.create_stack()
    stack.show_stack()