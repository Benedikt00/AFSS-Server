from flask import Blueprint, jsonify, render_template, request, get_template_attribute
from sqlalchemy import func
from extensions import db
from models import *
import random

from internal_logging import *

from config import Config

import json

from stack import instruction_stack_afss

from sps_communication import sps_com

afss_sps = sps_com(Config.CLIENT_SPS1_IP)
afss_sps.connect_to_sps("username", "password")

afss_stack = instruction_stack_afss()
afss_stack.create_stack()

# Create a Blueprint instance
api = Blueprint("api", __name__)


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

    current_location = Location.query.get_or_404(loc_now).current_location
    target_location = Location.query.get_or_404(loc_goal).target_location


def get_new_location(cont):
    filtered_locations = (
        db.session.query(Location)
        .filter_by(size=cont.size, occupation_status=False)
        .all()
    )
    # Return a random location from the filtered results
    if filtered_locations:
        return random.choice(filtered_locations)

    return None


@api.route("/afss_test", methods=["GET", "POST", "PUT", "PATCH"])
def afss_tset():

    request_data = {
        "method": request.method,
        "headers": dict(request.headers),
        "args": request.args.to_dict(),
        "form": request.form.to_dict(),
        "json": request.get_json(silent=True),
        "data": request.data.decode("utf-8"),
    }

    logcb(f"{json.dumps(request_data, indent=2)}")
    logcb(f"{request.method}, afss_test")
    return "200"


@api.route("/afss", methods=["GET", "POST"])
def afss():
    if request.method == "POST":
        req = request.get_json()

        # Storage Interrupt
        if "afss_return_request" in req.keys():
            afss_stack.request_box_return()
            return "200"

        # Storage Identification
        if "afss_return_data" in req.keys():
            code = req["afss_return"]["barcode"]
            cont = Container.query.filter_by(barcode=code).first()
            if not cont:
                return "404: Container not Found"

            afss_stack.insert_storing_operation(0, get_empty_location(cont))

            return "200"  # TODO

        if "next_bmos" in req.keys():
            return jsonify(afss_stack.get_current_bmos(int(req["next_bmos"])))

        if "new_operations" in req.keys():
            for pair in req["new_operations"]:
                afss_stack.norm_storing_operation(pair[0], pair[1])

            return "200"
        
        if "store_container" in req.keys():
            code = req["store_container"]
            cont = Container.query.filter_by(barcode=code).first()

            new_loc = get_new_location(cont)
            if not new_loc:
                return "418: No space Found"
            cont.target_location = new_loc.id

            new_loc.occupation_status = True
            afss_stack.insert_storing_operation(0, new_loc.id)
            return "Command has been sent."


        if "get_state" in req.keys():
            return 501

        if "set_state" in req.keys():
            afss_stack.read_state = req["set_state"]
            return "200"

        if "log_stack" in req.keys():
            return afss_stack.show_stack()

        if "return_ready" in req.keys():
            return afss_sps.read_variable("return_ready")

        if "afss_barcode_reading" in req.keys():
            barcode = afss_sps.read_variable("barcode")
            cont = Container.query.filter_by(barcode=int(barcode)).first()

            if not cont:
                return "Container not Found"

            stocks = Stock.query.filter_by(container = cont.id).all()

            h = []
            for st in stocks:
                quant = st.quantity
                r_quant = st.reserved_quantity

                art = Article.query.get_or_404(st.article)

                art_n = art.article_name
                pic = art.picture

                h.append(
                    {
                        "quantity": quant,
                        "reserved_quantity": r_quant,
                        "article_name": art_n,
                        "picture": pic,
                    }
                )

            return get_template_attribute("macros_for_return_box.html", "display_cont")(cont, h)

        return 501

    if request.method == "GET":
        return jsonify("415")
