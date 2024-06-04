from flask import Blueprint, jsonify, render_template, request
from sqlalchemy import func
from extensions import db
from models import *
import random

from config import Config

from stack import instruction_stack_afss

afss_stack = instruction_stack_afss()
afss_stack.create_stack()

# Create a Blueprint instance
api = Blueprint('api', __name__)


@api.route("/", methods=["GET", "POST"])
def index():
    return jsonify("This is the api of the F@ctory Ecosystem please do not break it")


def get_first_entry():
    entry = db.session.query(StackPrioAfss).order_by(StackPrioAfss.id).first()
    if entry:
        return entry

    entry = db.session.query(StackAfss).order_by(StackAfss.id).first()
    if entry:
        return entry

    # Return None if no entry is found in both tables
    return None

def make_move_instruction(entry):
    loc_now = entry.loc_now
    loc_goal = entry.loc_goal

    current_location = Location.query.get_or_404(loc_now)
    target_location = Location.query.get_or_404(loc_goal)


def get_empty_location(cont):
    filtered_locations = db.session.query(Location).filter_by(size=cont.size, occupation_status=False).all()
    # Return a random location from the filtered results
    if filtered_locations:
        return random.choice(filtered_locations)
    
    return None


@api.route("/afss", methods=["GET", "POST"])
def afss_stack():
    if request.method == "POST":
        req = request.get_json()

        #Storage Interrupt
        if "afss_return_request" in req.keys():
            afss_stack.request_box_return()
            return "200"

        #Storage Identification
        if "afss_return_data" in req.keys():
            code = req["afss_return"]["barcode"]
            cont = Container.query.filter_by(barcode = code).first()
            if not cont:
                return "400: Container not Found"
            
            afss_stack.insert_storing_operation(0, get_empty_location(cont))
            
            return "200" #TODO
        
        if "next_bmos" in req.keys():
            return jsonify(afss_stack.get_current_bmos(req["next_bmos"]))
        
        if "new_operations" in req.keys():
            for pair in req["new_operations"]:
                afss_stack.norm_storing_operation(pair[0], pair[1])
    
    if request.method == "GET":
        return jsonify("")




