from flask import Blueprint, jsonify, render_template

from config import Config

from internal_logging import *

visu = Blueprint("visu", __name__)

@visu.route("/afss", methods=["GET", "POST"])
def visu_afss():

    return render_template("visu/afss.html")
