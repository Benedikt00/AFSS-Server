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


@main.route("/pop")
def populate_database():
    # Add sample data to Article table

    areas = [
        Area(name="AFSS_S1", max_cont=200, allocated_cont=0),
        # Add more sample areas as needed
    ]
    db.session.bulk_save_objects(areas)

    locations = [
        # Location(area=1, category="PS", occupation_status=False, size="BM", position={"x": 1, "y": 2}), # LOG..Logistics, PS.. Permanent_storage, TS.. Temporary_storage
        # Location(area=1, category="PS", occupation_status=False, size="BM", position={"x": 2, "y": 3}), # BM..Box_medium
        # Add more sample locations as needed
    ]

    db.session.bulk_save_objects(locations)

    articles = [
        Article(
            article_name="Sample Article 1",
            article_description="Description 1",
            category="Category 1",
            groupes="Group 1",
            weight=100,
            picture="picture1.jpg",
        ),
        Article(
            article_name="Sample Article 2",
            article_description="Description 2",
            category="Category 2",
            groupes="Group 2",
            weight=200,
            picture="picture2.jpg",
        ),
        # Add more sample articles as needed
    ]
    db.session.bulk_save_objects(articles)

    # Add sample data to Area table

    containers = [
        Container(
            stocks=["1"],
            barcode=randint(100000000000, 999999999999),
            current_location=1,
            target_location=1,
            size="BM",
        ),
        Container(
            stocks=["2"],
            barcode=randint(100000000000, 999999999999),
            current_location=2,
            target_location=None,
            size="BM",
        ),
        # Add more sample containers as needed
    ]

    db.session.bulk_save_objects(containers)

    # Add sample data to Stock table
    stocks = [
        Stock(container=1, article=1, quantity=5),
        Stock(container=2, article=2, quantity=10),
        # Add more sample stocks as needed
    ]
    db.session.bulk_save_objects(stocks)

    db.session.commit()
    return jsonify({"message": "Data populated successfully"})


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


""" {# id INT PRIMARY KEY AUTO_INCREMENT,
    article_name VARCHAR(50),
    article_description TINYTEXT,
    category VARCHAR(20),
    groupes VARCHAR(50),
    weight INT,
    picture VARCHAR(30) #} """


class FormNewArticle(FlaskForm):
    article_name = StringField(
        "Article Name", validators=[DataRequired(), Length(max=50)]
    )
    article_description = TextAreaField(
        "Article Description", validators=[DataRequired(), Length(max=255)]
    )
    category = StringField("Category", validators=[DataRequired(), Length(max=20)])
    groupes = StringField("Groupes", validators=[DataRequired(), Length(max=50)])
    weight = IntegerField("Weight", validators=[DataRequired()])
    picture = StringField("Picture", validators=[Length(max=30)])
    submit = SubmitField("Artikel hinzufügen") #achtung wenn hier ter text geändert wird, muss dieser bei der auswertung auch geändert werden


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@main.route("/new_article", methods=['GET', "POST"])
def new_article():
    new_article_form = FormNewArticle()
    if request.method == "POST":
        logcb(request.form)
        if request.form['submit'] == "Artikel hinzufügen":
            req = request.form
            file = request.files['picture']

            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                if os.path.exists(os.path.join(Config.UPLOAD_FOLDER, filename)):
                    flash('File with same name already exists, please rename your file.')
                    return redirect(request.url)
                file.save(os.path.join(Config.UPLOAD_FOLDER, filename))
                flash('File successfully uploaded')
            else:
                flash('Allowed file types are png, jpg, jpeg, bmp')
                return redirect(request.url)
            
            new = Article(
            article_name = req['article_name'],
            article_description = req['article_description'],
            category = req['category'],
            groupes = req['groupes'],
            weight = int(req['weight']),
            picture = filename,
            )
            
            db.session.add(new)
            db.session.commit()

    return render_template("new_article.html", article_form = new_article_form)

def db_to_list(db_output):
    articles_list = []
    for article in db_output:
        article_dict = article.__dict__
        # Remove unwanted keys (e.g., internal SQLAlchemy attributes)
        article_dict.pop('_sa_instance_state', None)
        articles_list.append(article_dict)
    
    return articles_list

@main.route("/manage_db", methods=['GET'])
def manage_db():
    return render_template("manage_db.html")

@main.route("/manage_articles", methods=["GET", "POST"])
def edit_articles_db():
    if request.method == "POST":
        #logcb(request)
        if request.data: #check if request is json
            log.info(request.get_json())
            req = request.get_json()

            if "delete" in req.keys():
                log.info("")
                article = Article.query.get(int(req['delete']))
                img = article.picture
                
                if article:
                    db.session.delete(article)  # Delete the article from the session
                    db.session.commit()
                    articles_search = Article.query.limit(10).all()
                    return get_template_attribute("macros_for_manage_articles.html", "render_article_table")(articles_search)
                else:
                    return "400"
        

    
    articles_search = Article.query.limit(10).all()
    

    
    return render_template("manage_articles.html", articles = articles_search)

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
