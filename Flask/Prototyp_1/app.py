from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    get_template_attribute,
)
import json

from sql_connection_v2 import Database

import logging as log

fr_db = Database("mysql://root:112358@localhost:3306/test_db_bauteile", "db_factory_p1")

app = Flask(__name__)

"""
	zu empfehlen ist die vs code extension "better jinja" dann kann unten 
    rechts jinja html als sprahe verwendet werden. formattierung get zwar trozdem nicht, 
    aber es werden keine errors mehr gemeldet
"""


""" 
DEBUG: Detailed information, typically of interest only when diagnosing problems.
INFO: Confirmation that things are working as expected.
WARNING: An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.
ERROR: Due to a more serious problem, the software has not been able to perform some function.
CRITICAL
"""


log.basicConfig(
    format="%(levelname)s: %(message)s", encoding="utf-8", level=log.DEBUG
)  # filename='logs/app.log'


@app.route("/")
def root():
    # Redirect to "/sectionb"
    # return redirect(url_for('selection'))
    return render_template("index.html")


all_keys_for_search = fr_db.get_first_identifiers()


@app.route("/selection", methods=["get", "post"])
def selection():
    ls_form_values = []
    index_choose_placeholder = -1
    if request.method == "POST":

        data = request.form.to_dict()

        # handle request for next values
        if "form_values" in data.keys():
            ls_form_values = list(data["form_values"].split(","))

            all_keys_defined = False

            if "" not in ls_form_values:
                all_keys_defined = True

            if not all_keys_defined:
                key_next_search = fr_db.process_keys(ls_form_values)
                all_keys_for_search[key_next_search[-1]] = key_next_search[0]

            print(all_keys_for_search)

        # handle request for order
        if "order" in data.keys():
            print("Order this Component ", data)

    db_reply = fr_db.load_db_entries_from_keys(ls_form_values)

    if "" in ls_form_values:
        for i, el in enumerate(ls_form_values):
            if el == "":
                index_choose_placeholder = i
                break
    elif ls_form_values == []:
        index_choose_placeholder = 0

    return render_template(
        "selection.html",
        db_keys_1=all_keys_for_search,
        selected_values=ls_form_values,
        db_entrys_from_keys=db_reply,
        index_choose=index_choose_placeholder,
    )


@app.route("/manage_db", methods=["get", "post"])
def manage_db():
    db_entrys_to_display = fr_db.load_first_x_rows(10)
    min_max_cats = fr_db.get_keys_of_type_num()

    min_max_s = {}

    for cat in min_max_cats:
        min_max_s[cat] = fr_db.get_min_max_val(cat)

    # log.info(min_max_s)

    if request.method == "POST":
        log.info(f"manage dp recieved post request")
        data = request.form.to_dict()
        if "sort_db_entrys" in data.keys():
            inp = json.loads(data["sort_db_entrys"])
            # log.info(f'inp {type(inp)}: {inp}')
            sorted = fr_db.helper_sort_dict_by_value(inp["key"], inp["current_data"])
            log.info(f"sorted {type(sorted)}: {sorted}")

            template = render_template(
                "manage_db_data_list_macro.html", data_to_display=sorted
            )

            return (
                json.dumps({"success": True, "response": [template, sorted]}),
                200,
                {"ContentType": "application/json"},
            )
        # print(data)

        if "search_db" in data.keys():
            inp = json.loads(data["search_db"])
            # log.info(f'inp {type(inp)}: {inp}')
            searched = fr_db.load_db_search(inp)
            log.info(f"searched {type(searched)}: {searched}")
            template = render_template(
                "manage_db_data_list_macro.html", data_to_display=searched
            )
            # log.info(f'template {type(template)}: {template}')
            return (
                json.dumps(
                    {
                        "success": True,
                        "response": [template, [dict(row) for row in searched]],
                    }
                ),
                200,
                {"ContentType": "application/json"},
            )

    return render_template(
        "manage_db.html",
        data_to_display=db_entrys_to_display,
        kategories=fr_db.get_db_keys(),
        min_max_dict=min_max_s,
    )


@app.route("/manage_db/<id>", methods=["get", "post"])
def edit_db(id):
    if request.method == "POST":
        data = request.form.to_dict()

        if "change_db_entry" in data.keys():
            print(data["change_db_entry"])
            inp = json.loads(data["change_db_entry"])
            rep = sql_connect.edit_db_entry_after_cat(
                inp["id"], inp["cat_to_change"], inp["new_value"]
            )
            return (
                json.dumps({"success": True, "response": rep}),
                200,
                {"ContentType": "application/json"},
            )
    db_entry_for_id = fr_db.execute_query(
        f"SELECT * FROM {fr_db.table_name} WHERE id = {id}"
    )

    return render_template("edit_db.html", id=id, db_entry=db_entry_for_id)


@app.route("/new_entry", methods=["get", "post"])
def new_entry():
    if request.method == "POST":
        data = request.form.to_dict()
        log.info(f"data new entry post {type(data)}: {data}")

    return render_template("new_entry.html")


@app.route("/new_entry/afss", methods=["get", "post"])
def new_entry_afss():
    if request.method == "POST":
        data = request.form.to_dict()
        log.info(f"data new entry post {type(data)}: {data}")

    return render_template("storage_possibilities/afss.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route("/test")
def test():
    return render_template("test.html")


if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
