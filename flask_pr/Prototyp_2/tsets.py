from stack import instruction_stack_afss

from flask import Blueprint, jsonify, render_template, request


from config import Config
from extensions import db
from models import *
from afss_templates import logcb

testing = Blueprint("/test", __name__)

stack = instruction_stack_afss()
stack.create_stack()

@testing.route("/stack")
def stack_test():
    
    start = Location.query.get_or_404(30)

    end = Location.query.get_or_404(0)
    print(stack.show_stack())
    stack.create_order(stack.generate_path(start, end))
    print(type(Location.query.get_or_404(30)))

    print(stack.show_stack())


    return jsonify(stack.stack)

@testing.route("/stack/id", methods=["POST"])
def stack_test_id():
    if request.method == "POST":
        id = request.get_json()["id"]
        logcb(id)
    return jsonify(stack.get_current_bmos(int(id)))

@testing.route("/stack/_<id>", methods=['GET'])
def stack_test_ids(id):

    return jsonify(stack.get_current_bmos(int(id)))

@testing.route("/stack/show")
def show_stack():
    return jsonify(stack.stack)

@testing.route("/stack/run")
def run_sim():

    omnipotence = []
    for x in range(10):
        inst = stack.get_current_bmos(x)
        logcb(f"Id: {x}: {inst}")
        if inst:
            omnipotence.append(inst)

    return jsonify(omnipotence)