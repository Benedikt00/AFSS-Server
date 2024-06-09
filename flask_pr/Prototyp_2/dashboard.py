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

@dashb.route("/visu/afss", methods=["GET", "POST"])
def visu_afss():
    if request.method == "POST":
        if request.data:
            
            req = request.get_json()

            if "get_storage_flipper":
                return "501"

    return render_template("hw_control/afss_visu.html")

@dashb.route("/control/afss", methods=["GET", "POST"])
def control_afss():
    if request.method == "POST":
        if request.data:    
            req = request.get_json()

            if "connect_to_client" in req.keys():
                ip = req["connect_to_client"]["ip"]
                #start_time = req["connect_to_client"]["start_time"]
                start_time = round(time.time()) * 1000
                user = req["connect_to_client"]["creds"]["username"]
                password = req["connect_to_client"]["creds"]["password"]
            
                if ip != Config.CLIENT_SPS1_IP:
                    debug_connection.ip_address = ip

                status = debug_connection.connect_to_sps(user, password)

                #logcb(f"start {start_time}, now: {time.time()}")

                ping = round(time.time()) * 1000 - start_time
                return get_template_attribute("hw_control/macros_for_afss_control.html", "connection_return")(status, ping, debug_connection.session_token)

            if "ping" in req.keys():
                debug_connection.ping_sps()
                return "200"
            
            if "enable_testwindow" in req.keys():
                return get_template_attribute("hw_control/macros_for_afss_control.html", "testwindow")
        
    return render_template("hw_control/afss_control.html", ip = Config.CLIENT_SPS1_IP)
    


@dashb.route("/visu/afss/api", methods=["GET", "POST"])
def afss_api():
    return "501"