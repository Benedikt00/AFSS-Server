from flask import Blueprint, jsonify, render_template, request, get_template_attribute

from config import Config

from internal_logging import *

from sps_communication import sps_com
import requests

import time

dashb = Blueprint("dashb", __name__)

debug_connection = sps_com(Config.CLIENT_SPS1_IP)


@dashb.route("/")
def index():
    return render_template("hw_control/dashboard.html")


# TODO: Implement
@dashb.route("/visu/afss", methods=["GET", "POST"])
def visu_afss():
    if request.method == "POST":
        if request.data:

            req = request.get_json()

            if "get_storage_flipper" in req.keys():
                return "501"
            

    return render_template("visu/afss_visu.html")


@dashb.route("/control/afss", methods=["GET", "POST"])
def control_afss():
    if request.method == "POST":
        if request.data:
            req = request.get_json()

            if "connect_to_client" in req.keys():
                logcb("Connect to client")
                ip = req["connect_to_client"]["ip"]

                # start_time = req["connect_to_client"]["start_time"]/1000
                start_time = round(time.time())
                user = req["connect_to_client"]["creds"]["username"]
                password = req["connect_to_client"]["creds"]["password"]

                if (ip != Config.CLIENT_SPS1_IP) or (
                    debug_connection.ip_address != Config.CLIENT_SPS1_IP
                ):
                    logcb(f"changed ip {ip}")
                    debug_connection.new_ip_address(ip)

                status = debug_connection.connect_to_sps(user, password)

                logcb(f"status {status}")

                ping = round(time.time()) - start_time
                return get_template_attribute(
                    "hw_control/macros_for_afss_control.html", "connection_return"
                )(str(status), ping, debug_connection.session_token)

            if "ping" in req.keys():
                debug_connection.ping_sps()
                return "200"

            if "enable_testmode" in req.keys():
                logcb("testmode")
                status = debug_connection.enable_testmode()
                return get_template_attribute(
                    "hw_control/macros_for_afss_control.html", "testwindow"
                )(status)

            if "update_position" in req.keys():
                logcb("update_position")
                posis = req["update_position"]
                x = posis["x"]
                y = posis["y"]
                z = posis["z"]
                a = posis["a"]  # ausfahrer
                f = posis["f"]  # förderband

                debug_connection.write_variable("pos_x", x)
                debug_connection.write_variable("pos_y", y)
                debug_connection.write_variable("pos_z", z)
                debug_connection.write_variable("pos_ausfahrer", a)
                debug_connection.write_variable("pos_förderband", f)

    return render_template("hw_control/afss_control.html", ip=Config.CLIENT_SPS1_IP)


@dashb.route("/visu/afss/api", methods=["GET", "POST"])
def afss_api():
    return "501"
