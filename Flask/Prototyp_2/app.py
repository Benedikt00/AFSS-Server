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

from search_logic import search_query

# db = SQLAlchemy(app)


main = Blueprint("main", __name__)


"""
	zu empfehlen ist die vs code extension "better jinja" dann kann unten 
    rechts "jinja html" als sprache verwendet werden. formattierung get zwar trozdem nicht, 
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
    return render_template("index.html")


@main.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@main.route("/test")
def test():
    return render_template("test.html")

        

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

            return 200

        return 400

    groupes = PrimaryGroup.query.all()

    categories = Categories.query.all()

    return render_template("new_article.html", groupes=groupes, categories=categories)

@main.route('/get_image/<image_name>')
def get_image(image_name):
    #logcb(f"{Config.UPLOAD_FOLDER} {image_name}  {os.path.join(Config.UPLOAD_FOLDER, image_name)}")
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
            
            if "fancy_query" in req.keys():
                query = req["fancy_query"]
                #with main.test_client() as client:
    
                data_list = search_query(query)

                ids = [sublist[1] for sublist in data_list]

                # Construct a custom SQL query to retrieve elements from the database table
                # and sort them based on the order of IDs in the 'ids' list
                results = Article.query.filter(Article.id.in_(ids)).order_by(
                    db.func.field(Article.id, *ids)
                ).all()

                return get_template_attribute("macros_for_search_articles.html", "display_field")(results)


        return 400

    f_ten = Article.query.limit(Config.QUERY_LIMIT_SOFT).all()

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
            
            if "gen_stock" in req.keys():
                logcb(req['gen_stock'])
                return get_template_attribute("macros_for_add_stock.html", "generated_stock")(
                    Article.query.get_or_404(int(req["gen_stock"]["article"])).article_name,
                    req["gen_stock"]["quantity"],
                    Article.query.get_or_404(int(req["gen_stock"]["article"])).picture,
                    req["gen_stock"]["barcode"]

                )

            if "add_stock" in req.keys():
                dt = req["add_stock"]
                new = Stock(
                    container = db.session.query(Container).filter_by(barcode=dt['barcode']).first().id,
                    article = dt['article'],
                    quantity = dt['quantity']
                )

                db.session.add(new)
                db.session.commit()
                return "Sucsess"



    return render_template("add_stock.html")


@main.route("/add_container", methods=["GET", "POST"])
def add_container():
    if request.method == "POST":
        if request.data:
            req = request.get_json()
            if "get_barcode" in req.keys():
                # TODO:
                return str(randint(100000000, 1000000000 - 1))
            
            if "add_container" in req.keys():
                bc = req['add_container']["barcode"]
                size = req['add_container']["size"]
                exists = db.session.query(Container).filter_by(barcode=bc).first() is not None

                if not exists:
                    new_cont = Container(
                        barcode = bc,
                        size = size,
                        current_location = 0
                    )

                    db.session.add(new_cont)
                    db.session.commit()

                    return "Successfully added"
                
                else:
                    return "Barcode already exists"
            

    return render_template("add_container.html")

import xml.etree.ElementTree as ET

@main.route("/add_area", methods=["GET", "POST"])
def add_area():
    if request.method == "POST":
        log.info(request.form)
        log.info(request.files)
        if "gen_stuff" in request.form.keys():
            if 'file' in request.files.keys():
                log.info(f'request.files {type(request.files)}: {request.files}')
                file = request.files['file']

                if file.filename == '':
                    return jsonify({'error': 'No selected file'})

                file_contents = file.read().decode('utf-8')
                log.info(f'file_contents {type(file_contents)}: {file_contents}')
                try:
                    xml_root = ET.fromstring(file_contents)
                except Exception as e:
                    return e
                
                num_rows = int(xml_root.findall("gen_data")[0].attrib['num_rows'])
                num_cols = int(xml_root.findall("gen_data")[0].attrib['num_cols'])
                title = xml_root.attrib['title']

                # Initialize variables to track the lowest and highest x and y values
                lowest_x = float('inf')
                highest_x = float('-inf')
                lowest_y = float('inf')
                highest_y = float('-inf')

                total_locations = 0
                for row in xml_root.findall('row'):
                    for location in row.findall('location'):
                        x = float(location.attrib['x'])
                        y = float(location.attrib['y'])
                        total_locations += 1

                        lowest_x = min(lowest_x, x)
                        highest_x = max(highest_x, x)
                        lowest_y = min(lowest_y, y)
                        highest_y = max(highest_y, y)
                
                data = {"num_rows": num_rows, "num_cols": num_cols, "title": title, "num_locations": total_locations, "min": f"{lowest_x, lowest_y}", "max": f"{highest_x, highest_y}"}
                log.info(f'data {type(data)}: {data}')

                return get_template_attribute("macros_for_add_area.html", "area_stats")(data)

            else:
                return jsonify({'error': 'No file part'})
            
        if "add_all" in request.form.keys():
            if 'file' in request.files.keys():
                log.info(f'request.files {type(request.files)}: {request.files}')
                file = request.files['file']

                if file.filename == '':
                    return jsonify({'error': 'No selected file'})

                file_contents = file.read().decode('utf-8')
                log.info(f'file_contents {type(file_contents)}: {file_contents}')
                try:
                    xml_root = ET.fromstring(file_contents)
                except Exception as e:
                    return e

                area_name = xml_root.attrib['title']
                log.info(f'area_name {type(area_name)}: {area_name}')

                new_area = Area(name=area_name, allocated_cont = 0)


                db.session.add(new_area)
                db.session.commit()


                total_locations = 0
                for row in xml_root.findall('row'):
                    for location in row.findall('location'):
                        
                        new_location = Location(
                            area = new_area.id,
                            category = location.attrib['category'], 
                            occupation_status = False, 
                            size = "BM",  # * Set as needed
                            position = {"x": int(location.attrib['x']), "y": int(location.attrib['y']), "z": 0}  
                        )
                        total_locations += 1

                        db.session.add(new_location)

                # Commit the changes to the database
                new_area.max_cont = total_locations

                db.session.commit()
                
                return jsonify("Worx")

    return render_template("add_area.html")

@main.route("/del")
def delete_data():
    try:
        db.session.query(Area).delete()

        # This SQL command resets the auto-increment counter for the table to 1
        for table in ["area"]:
            db.session.execute(text(f"ALTER TABLE {table} AUTO_INCREMENT = 0"))
            pass

        db.session.commit()
    except Exception as e:
        log.info(e)
        db.session.rollback()

    return jsonify({"message": "Data deleted successfully"})



if __name__ == "__main__":
    import __init__

    app = __init__.create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
