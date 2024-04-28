from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    get_template_attribute,
    session,
    Blueprint,
    flash,
    send_from_directory,
)
import json
import xmltodict
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring

import logging as log

import os

log.basicConfig(
    format="%(levelname)s: %(message)s", encoding="utf-8", level=log.DEBUG
)  # filename='logs/app.log'

class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

def logcb(var):
    log.info(f"{type(var)}: {bcolors.OKBLUE} {var} {bcolors.ENDC}")


afss_templates = Blueprint('afss_templates', __name__)

TEMP_FILE_PATH = "./Prototyp_2/storage_templates/temp.xml"


@afss_templates.route("/storage_templates", methods=["GET", "POST"])
def storage_templates():

    logcb(request.form)
    logcb(request)
    if request.method == "POST":
        if request.data:
            log.info(request.get_json())
        if "num_rows" in request.form.keys():
            log.info(request.form)
            log.info("rows")
            num_rows = int(request.form["num_rows"])
            num_cols = int(request.form["num_cols"])
            row_spacing = int(request.form["row_spacing"])
            col_spacing = int(request.form["col_spacing"])
            x_spacers = json.loads(request.form["spacers"].replace("'", '"'))

            x_zero = int(request.form["x_zero"])
            y_zero = int(request.form["x_zero"])

            xml_root = ET.Element("storage", title=request.form["title"])

            con_x_spacers = [
                {key: str(value) for key, value in d.items()} for d in x_spacers
            ]  # js braucht json in diesem format

            con_x_spacers = str(con_x_spacers).replace("'", "\\'")

            data = ET.SubElement(
                xml_root,
                "gen_data",
                num_rows=str(num_rows),
                num_cols=str(num_cols),
                row_spacing=str(row_spacing),
                col_spacing=str(col_spacing),
                x_spacers=str(con_x_spacers),
            )

            for i in range(num_rows):
                row = ET.SubElement(
                    xml_root, "row", id=str(i), y=str((i * row_spacing) + y_zero)
                )

                x_spaceing = 0

                x_spacers_to_do = x_spacers[
                    :
                ]  # wtf, hier wird eine kopie erstellt, da sonst auch das originalvalue mit remove() bearbeitet wird

                # log.info(f'x_spacers_to_do {type(x_spacers_to_do)}: {x_spacers_to_do}')

                for j in range(num_cols + len(x_spacers)):
                    used = False
                    for el in x_spacers_to_do:
                        if el["x"] == j:

                            x_spaceing += el["width"]
                            x_spacers_to_do.remove(el)
                            spacer = ET.SubElement(
                                row,
                                "spacer",
                                id=str(j),
                                x=str(j * col_spacing + x_zero + x_spaceing),
                                width=str(el["width"]),
                            )
                            used = True
                            break
                        break
                    if not used:
                        location = ET.SubElement(
                            row,
                            "location",
                            id=str(j),
                            x=str(j * col_spacing + x_zero + x_spaceing),
                            y=str((i * row_spacing) + y_zero),
                            category="PS",
                        )

            tree = ET.ElementTree(xml_root)
            tree.write(TEMP_FILE_PATH)

            # log.info(xmltodict.parse(tostring(xml_root, encoding='unicode', method="xml")))

            return render_template(
                "afss_templates.html",
                num_rows=num_rows,
                num_cols=num_cols,
                row_spacing=row_spacing,
                col_spacing=col_spacing,
                x_spacers=x_spacers,
                x_zero=x_zero,
                y_zero=y_zero,
                xml=xmltodict.parse(
                    tostring(xml_root, encoding="unicode", method="xml")
                ),
                edit_form_bool=0,
            )

        if "xy" in request.get_json():
            id_x = request.get_json()["xy"]["id_x"]
            id_y = request.get_json()["xy"]["id_y"]
            log.info(id_x)
            log.info(id_y)
            # edit_form = Edit_entry(param1_default=id_x, param2_default=id_y)

            tree = ET.parse("storage_templates/temp.xml")
            root = tree.getroot()

            for row in root.findall("row"):
                if int(row.get("id")) == int(id_y):
                    for element in row.findall("*"):
                        if int(element.get("id")) == int(id_x):
                            log.info(f"{id_x}_found")
                            break
                    break

            y_id = row.get("id")
            y_cord_row = row.get("y")

            if element.tag == "location":
                cat = element.get("category")
                x_id = element.get("id")
                y_cord = element.get("y")
                x_cord = element.get("x")
                dt = {
                    "type": "location",
                    "y_id": y_id,
                    "x_id": x_id,
                    "y_cord": y_cord,
                    "x_cord": x_cord,
                    "category": cat,
                }

                return get_template_attribute("temp_edit.html", "edit_loc")(
                    "Location", x_id, y_id, x_cord, y_cord, cat
                )

            else:
                width = element.get("width")
                x_id = element.get("id")
                x_cord = element.get("x")
                dt = {
                    "type": "spacer",
                    "y_id": y_id,
                    "x_id": x_id,
                    "x_cord": x_cord,
                    "width": width,
                }

                return get_template_attribute("temp_edit.html", "edit_spc")(
                    "Spacer", x_id, y_id, x_cord, width
                )
        if "ch" in request.get_json():
            logcb(request.get_json())
            data = request.get_json()
            log.info("ch")
            tree = ET.parse(TEMP_FILE_PATH)
            root = tree.getroot()

            for row in root.findall("row"):
                if int(row.get("id")) == int(data["id_y"]):
                    for element in row.findall("*"):
                        if int(element.get("id")) == int(data["id_x"]):
                            logcb(f"_found")
                            if data["name"] == "Location":
                                element.set("x", (data["x"]))
                                element.set("y", (data["y"]))
                                element.set("category", (data["ch"]))
                            if data["name"] == "Spacer":
                                element.set("x", (data["x"]))
                                element.set("category", (data["ch"]))
                            break
                    break

            tree.write(TEMP_FILE_PATH)
            return "200"

    return render_template(
        "afss_templates.html",
        num_rows=3,
        num_cols=5,
        row_spacing=80,
        col_spacing=160,
        x_spacers=[{"x": 2, "width": 45}, {"x": 4, "width": 45}],
        x_zero=30,
        y_zero=20,
    )
