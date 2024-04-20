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

from sqlalchemy import text, sql, select, exists, func
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user,
)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import (
    DataRequired,
    InputRequired,
    Length,
    ValidationError,
    NumberRange,
)

from extensions import db
from extensions import login_manager
from extensions import bcrypt
from models import *

from random import randint

from time import sleep
import os
from werkzeug.utils import secure_filename

from config import Config

# db = SQLAlchemy(app)


main = Blueprint("main", __name__)


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


@main.route("/")
def root():
    # Redirect to "/sectionb"
    # return redirect(url_for('selection'))
    return render_template("index.html")


@main.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@main.route("/test")
def test():
    return render_template("test.html")

class Edit_entry(FlaskForm):
    param1 = StringField("Parameter 1")
    param2 = StringField("Parameter 2")
    submit = SubmitField("Submit")

    # Constructor to set default values
    def __init__(self, param1_default="", param2_default="", *args, **kwargs):
        super(Edit_entry, self).__init__(*args, **kwargs)
        self.param1.default = param1_default
        self.param2.default = param2_default
        self.process()


@main.route("/storage_templates", methods=["GET", "POST"])
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

            xml_root = ET.Element("storage", title="afss_2")

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
            tree.write("storage_templates/afss_2.xml")

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

            tree = ET.parse("storage_templates/afss_2.xml")
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
            tree = ET.parse("storage_templates/afss_2.xml")
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

            tree.write("storage_templates/afss_2.xml")
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


class FormNewArticle(FlaskForm):
    article_name = StringField("Article Name", validators=[Length(max=50)])
    article_description = TextAreaField(
        "Article Description", validators=[Length(max=255)]
    )

    weight = IntegerField("Weight")
    picture = StringField("Picture", validators=[Length(max=30)])


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS
    )


added_attributes = []


def string_to_list(string):
    cleaned_string = string.strip("[]").replace(", ", ",")
    log.info(f"cleaned_string {type(cleaned_string)}: {cleaned_string}")
    # Split the string by commas and convert each element to an integer
    list_from_string = [(item.strip("'")) for item in cleaned_string.split(",")]

    return list_from_string


@main.route("/new_article", methods=["GET", "POST"])
def new_article():
    # new_article_form = FormNewArticle()

    if request.method == "POST":
        logcb(request.form)

        if request.data:
            req = request.get_json()

            if "get_secs" in req.keys():
                title = req["get_secs"]
                secs = SecondaryGroup.query.filter_by(prim_title=title).all()
                return get_template_attribute(
                    "macros_for_new_articles.html", "render_sec_groupes_for_prim"
                )(secs)

            if "deselect" in req.keys():
                pass  # TODO

            if "select_category" in req.keys():
                selected_cat = req["select_category"]

                db_cat = Categories.query.filter_by(title=selected_cat).first()

                prefixes = string_to_list(db_cat.prefixes)
                log.info(f"prefixes {type(prefixes)}: {prefixes}")
                unit = db_cat.unit

                return get_template_attribute(
                    "macros_for_new_articles.html", "further_cat"
                )(prefixes, unit)

            if "new_cat" in req.keys():
                data = req["new_cat"]

                added_attributes.append(data)

                return get_template_attribute(
                    "macros_for_new_articles.html", "list_cats"
                )(added_attributes)

            if "del_cat" in req.keys():
                element = eval(req["del_cat"])
                log.info(f"element {type(element)}: {element}")
                log.info(added_attributes)
                added_attributes.remove(element)

                return get_template_attribute(
                    "macros_for_new_articles.html", "list_cats"
                )(added_attributes)

            if "new_article" in req.keys():
                data = req["new_article"]
                logcb(f"data {type(data)}: {data}")

            logcb(req)

            return 400

        logcb(request.form)

        if request.form["new_article"]:
            req = request.form["new_article"]  # .get_json()
            log.info(f"req {type(req)}: {req}")

            file = request.files["image"]

            if file.filename == "":
                flash("No selected file")
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                if os.path.exists(os.path.join(Config.UPLOAD_FOLDER, filename)):
                    flash(
                        "File with same name already exists, please rename your file."
                    )
                    return redirect(request.url)
                file.save(os.path.join(Config.UPLOAD_FOLDER, filename))
                flash("File successfully uploaded")
            else:
                flash("Allowed file types are png, jpg, jpeg, bmp")
                return redirect(request.url)

            """ new = Article(
                article_name=req["article_name"],
                article_description=req["article_description"],
                category=req["category"],
                groupes=req["groupes"],
                weight=int(req["weight"]),
                picture=filename,
            )

            db.session.add(new)
            db.session.commit() """

            return 200

        return 400

    groupes = PrimaryGroup.query.all()

    categories = Categories.query.all()

    return render_template("new_article.html", groupes=groupes, categories=categories)

@main.route('/get_image/<image_name>')
def get_image(image_name):
    return send_from_directory(Config.UPLOAD_FOLDER, image_name)

@main.route("/add_article", methods=["POST"])
def add_article():

    #log.info(request.form.keys())

    if 'image' not in request.files or 'new_article' not in request.form.keys(): #nicht daran gewöhnen dass da alles 3 mal überprüft wird, das ist nur so weil dass die KI so generiert hat
        return jsonify({'error': 'Missing required parameters'}), 200
    image_file = request.files["image"]
    # Save the image file

    if image_file.filename == "":
        return("No selected file")

    if image_file and allowed_file(image_file.filename):

        filename = secure_filename(image_file.filename)
        if os.path.exists(os.path.join(Config.UPLOAD_FOLDER, filename)):
            return "File with same name already exists, please rename your file."
    else:
        filename = ""
    # Get the JSON data
    # Parse JSON data
    new_article_data = request.form['new_article']
    logcb(f'new_article_data {type(new_article_data)}: {new_article_data}')
    # Parse JSON data
    try:
        article = json.loads(new_article_data)
        log.info(f'article {type(article)}: {article}')
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON in new_article parameter'}), 200


    try:

        name = article['name']
        description = article['description']
        weight = article['weight']
        img = filename
        prim_groupe = article['prim_groupe']
        sec_groupe = article['sec_groupe']
        categories = (article['categories'])
    
    except Exception:
        return jsonify({'error': 'it seems as though there is one or more parameters missing'}), 200

    new = Article(
        article_name = name,
        article_description = description,
        groupes = [prim_groupe, sec_groupe],
        weight = weight,
        category = categories,
        picture = img
    )
    
    db.session.add(new)
    db.session.commit()



    image_file.save(os.path.join(Config.UPLOAD_FOLDER, filename))

    added_attributes = []

    return "File successfully uploaded"


def db_to_list(db_output):
    articles_list = []
    for article in db_output:
        article_dict = article.__dict__
        # Remove unwanted keys (e.g., internal SQLAlchemy attributes)
        article_dict.pop("_sa_instance_state", None)
        articles_list.append(article_dict)

    return articles_list


@main.route("/manage_db", methods=["GET"])
def manage_db():
    return render_template("manage_db.html")


def search_record_by_value(value, model, column_name):
    # Query the database for the record matching the value in the specified column
    records = model.query.filter(getattr(model, column_name) == value)
    return records


@main.route("/manage_articles", methods=["GET", "POST"])
def edit_articles_db():
    lim = 10
    if request.method == "POST":
        # logcb(request)
        if request.data:  # check if request is json
            log.info(request.get_json())
            req = request.get_json()

            if "delete" in req.keys():
                log.info("")
                article = Article.query.get(int(req["delete"]))
                img = article.picture

                if article:
                    file = os.path.join(Config.UPLOAD_FOLDER, img)
                    if os.path.exists(file):
                        pass
                        os.remove(file)
                    db.session.delete(article)  # Delete the article from the session
                    db.session.commit()
                    articles_search = Article.query.limit(lim).all()
                    return get_template_attribute(
                        "macros_for_manage_articles.html", "render_article_table"
                    )(articles_search)
                else:
                    return "400"

            if "changes" in req.keys():
                changes = req["changes"]
                log.info(f"changes {type(changes)}: {changes}")
                for change in changes:
                    log.info(f"change {type(change)}: {change}")
                    id = list(change.keys())[0]
                    # logcb(f'id {type(id)}: {id}')
                    record = Article.query.get_or_404(int(id))

                    column_name = list(change[id].keys())[0]

                    if hasattr(record, column_name):
                        # Update the text in the column dynamically
                        setattr(record, column_name, change[id][column_name])

                        # Commit the changes to the database
                        db.session.commit()

                        articles_search = Article.query.limit(lim).all()

                    else:
                        return jsonify({"error": "Column does not exist"}), 400
                return get_template_attribute(
                    "macros_for_manage_articles.html", "render_article_table"
                )(articles_search)

            if "search" in req.keys():
                search = req["search"]
                column_name = list(search.keys())[0]
                value = search[column_name]

                column = getattr(Article, column_name)

                results = Article.query.filter(column.like("%" + value + "%"))

                return get_template_attribute(
                    "macros_for_manage_articles.html", "render_article_table"
                )(results)

    articles_search = Article.query.limit(lim).all()

    return render_template("manage_articles.html", articles=articles_search)


@main.route("/manage_stock", methods=["GET", "POST"])
def edit_stocks_db():

    stock = Stock.query.limit(10).all()

    return render_template("manage_stock.html", stocks=stock)


@main.route("/manage_categories", methods=["GET", "POST"])
def edit_categories_db():

    if request.method == "POST":
        log.info(request.form)
        if request.data:  # check if request is json
            log.info(request.get_json())
            req = request.get_json()

            if "new_cat" in req.keys():
                n_c = req["new_cat"]
                log.info(n_c)

                prefs = n_c["prefixes"]
                log.info(prefs)

                # if not isinstance(prefs, list):
                #    flash("Prefixes in wrong format must be ['m', 'µ']")

                #    cats = Categories.query.all()
                #    return get_template_attribute("macros_for_manage_categories.html", "render_categories_table")(cats)

                new_cat = Categories(
                    title=n_c["title"], unit=n_c["unit"], prefixes=prefs
                )

                db.session.add(new_cat)
                db.session.commit()

                cats = Categories.query.all()
                return get_template_attribute(
                    "macros_for_manage_categories.html", "render_categories_table"
                )(cats)

            if "delete" in req.keys():
                del_title = req["delete"]
                cat = Categories.query.get(del_title)

                db.session.delete(cat)
                db.session.commit()

                cats = Categories.query.all()
                return get_template_attribute(
                    "macros_for_manage_categories.html", "render_categories_table"
                )(cats)

            if "changes" in req.keys():
                changes = req["changes"]
                log.info(f"changes {type(changes)}: {changes}")
                for change in changes:

                    title = list(change.keys())[0]

                    record = Categories.query.get_or_404(title)

                    column_name = list(change[title].keys())[0]

                    if hasattr(record, column_name):
                        # Update the text in the column dynamically
                        setattr(record, column_name, change[title][column_name])

                        # Commit the changes to the database
                        db.session.commit()
                        cats = Categories.query.all()

                    else:
                        return jsonify({"error": "Column does not exist"}), 400

                return get_template_attribute(
                    "macros_for_manage_categories.html", "render_categories_table"
                )(cats)

    cats = Categories.query.all()

    return render_template("manage_categories.html", cats=cats)


@main.route("/manage_groupes", methods=["GET", "POST"])
def edit_groupes_db():

    if request.method == "POST":
        log.info(request.form)
        if request.data:  # check if request is json
            log.info(request.get_json())
            req = request.get_json()

            if "new_prim_group" in req.keys():
                logcb(req["new_prim_group"])
                new_p_g = PrimaryGroup(title=req["new_prim_group"])

                db.session.add(new_p_g)
                db.session.commit()

                prim_groupes = PrimaryGroup.query.all()

                return get_template_attribute(
                    "macros_for_manage_groupes.html", "render_prim_groupes_table"
                )(prim_groupes)

            if "new_sec_group" in req.keys():
                prim_g = req["new_sec_group"]["primary_group"]
                sec_g = req["new_sec_group"]["secondary_group"]

                new_s_g = SecondaryGroup(prim_title=prim_g, title=sec_g)

                db.session.add(new_s_g)
                db.session.commit()

                prim_groupes = PrimaryGroup.query.all()

                return get_template_attribute(
                    "macros_for_manage_groupes.html", "render_prim_groupes_table"
                )(prim_groupes)

            if "secs_for_prim" in req.keys():
                prim_g = req["secs_for_prim"]

                secs = SecondaryGroup.query.filter_by(prim_title=prim_g).all()
                logcb(f"secs {type(secs)}: {secs}")
                return get_template_attribute(
                    "macros_for_manage_groupes.html", "secondars"
                )(
                    secs, prim_g
                )  # prim_g falls noch keine untergruppen vorhanden

            if "delete_prim" in req.keys():
                del_title = req["delete_prim"]
                gp = PrimaryGroup.query.get(del_title)

                db.session.delete(gp)
                db.session.commit()

                prim_groupes = PrimaryGroup.query.all()

                return get_template_attribute(
                    "macros_for_manage_groupes.html", "render_prim_groupes_table"
                )(prim_groupes)

            if "changes" in req.keys():
                changes = req["changes"]

                # TODO
                prim_groupes = PrimaryGroup.query.all()

                return get_template_attribute(
                    "macros_for_manage_groupes.html", "render_prim_groupes_table"
                )(prim_groupes)

    prim_groupes = PrimaryGroup.query.all()

    return render_template("manage_groupes.html", prim_groupes=prim_groupes)

def search_articles_db_groupes(group_names):
    if isinstance(group_names, str):
        # Search for articles where the first category matches the group name
        results = Article.query.filter(Article.groupes[0] == group_names).all()
        return results
    elif isinstance(group_names, list):
        # Search for articles where any category matches any of the group names
        filters = [func.json_extract(Article.groupes, f"$[{index}]") == group_name for index, group_name in enumerate(group_names)]
        results = Article.query.filter(*filters).all()
    else:
        # Invalid input
        results = []

    return results

#haha des wird ja was werden
@main.route("/search_articles_db_interaction", methods=["GET", "POST"])
def search_articles_db_interaction():
    logcb(request)
    if request.method == "POST":
        if request.data:
            req = request.get_json()
            log.info(f'req {type(req)}: {req}')

            if "get_primary_groupes" in req.keys():
                return get_template_attribute("macros_for_search_articles.html", "render_primary_groupes")(PrimaryGroup.query.all())

            if "get_secs_for_prim" in req.keys():
                prim = req['get_secs_for_prim']

                secs = SecondaryGroup.query.filter_by(prim_title=prim).all()

                return get_template_attribute("macros_for_search_articles.html", "render_for_secs")(secs, PrimaryGroup.query.all())
            
            if "search" in req.keys():

                search = req['search']
                logcb(search)
                
                first_search_in_db = False

                if "extend_search" in search.keys():
                    extend_search = search['extend_search']
                    show_all = search['show_all']


                if ("search_with_groupes" in search.keys()) and not first_search_in_db:

                    articles = search_articles_db_groupes(search["search_with_groupes"])
                    if not articles in ["", [], 0]:
                        return get_template_attribute("macros_for_search_articles.html", "display_field")(articles)

                if ("string_search" in search.keys()) and not first_search_in_db:
                    keyword = search['string_search']
                    results = Article.query.filter((Article.article_name.like(f'%{keyword}%')) | (Article.article_description.like(f'%{keyword}%'))).all()
                    return get_template_attribute("macros_for_search_articles.html", "display_field")(results)
                    
                if ("attributes" in search.keys()):
                    #TODO
                    pass


        return 400

    f_ten = Article.query.limit(10).all()

    return get_template_attribute("macros_for_search_articles.html", "display_field")(f_ten)


@main.route("/search_articles", methods=["GET", "POST"])
def search_articles():
    return render_template("search_articles.html")


@main.route("/add_stock", methods=['GET', "POST"])
def add_stock():
    if request.method == "POST":
        if request.data:
            req = request.get_json()
            log.info(f'req {type(req)}: {req}')

            if "get_container_code" in req.keys():
                #TODO:
                random_container = Container.query.order_by(func.random()).first()
                return jsonify({"status_message": "random", "code": str(random_container.barcode)})

    return render_template("add_stock.html")


@main.route("/add_container", methods=["GET", "POST"])
def add_container():
    if request.method == "POST":
        if request.data:
            req = request.get_json()
    return render_template("add_container.html")




@main.route("/del")
def delete_data():
    try:
        db.session.query(Stock).delete()
        db.session.query(Container).delete()
        db.session.query(Location).delete()
        db.session.query(Area).delete()
        db.session.query(Article).delete()

        # This SQL command resets the auto-increment counter for the table to 1
        for table in ["stock", "container", "location", "area", "article"]:
            db.session.execute(text(f"ALTER TABLE {table} AUTO_INCREMENT = 1"))
            pass

        db.session.commit()
    except Exception as e:
        log.info(e)
        db.session.rollback()

    return jsonify({"message": "Data deleted successfully"})



if __name__ == "__main__":
    import __init__

    __init__.create_app()
