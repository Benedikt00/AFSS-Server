
from models import *
from extensions import db
import os
from config import Config
import logging as log

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

# Create a Blueprint instance
manage_db = Blueprint('manage_db', __name__)


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


@manage_db.route("/", methods=["GET"])
def index():
    return render_template("db_management/manage_db.html")


def search_record_by_value(value, model, column_name):
    # Query the database for the record matching the value in the specified column
    records = model.query.filter(getattr(model, column_name) == value)
    return records


@manage_db.route("/articles", methods=["GET", "POST"])
def edit_articles_db():
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
                    articles_search = Article.query.limit(Config.QUERY_LIMIT_SOFT).all()
                    return get_template_attribute(
                        "db_management/macros_for_manage_articles.html", "render_article_table"
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

                        articles_search = Article.query.limit(Config.QUERY_LIMIT_SOFT).all()

                    else:
                        return jsonify({"error": "Column does not exist"}), 400
                return get_template_attribute(
                    "db_management/macros_for_manage_articles.html", "render_article_table"
                )(articles_search)

            if "search" in req.keys():
                search = req["search"]
                column_name = list(search.keys())[0]
                value = search[column_name]

                column = getattr(Article, column_name)

                results = Article.query.filter(column.like("%" + value + "%"))

                return get_template_attribute(
                    "db_management/macros_for_manage_articles.html", "render_article_table"
                )(results)

    articles_search = Article.query.limit(Config.QUERY_LIMIT_SOFT).all()

    return render_template("db_management/manage_articles.html", articles=articles_search)


@manage_db.route("/stock", methods=["GET", "POST"])
def edit_stocks_db():

    stock = Stock.query.limit(10).all()

    return render_template("db_management/manage_stock.html", stocks=stock)


@manage_db.route("/categories", methods=["GET", "POST"])
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
                    "db_management/macros_for_manage_categories.html", "render_categories_table"
                )(cats)

            if "delete" in req.keys():
                del_title = req["delete"]
                cat = Categories.query.get(del_title)

                db.session.delete(cat)
                db.session.commit()

                cats = Categories.query.all()
                return get_template_attribute(
                    "db_management/macros_for_manage_categories.html", "render_categories_table"
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
                    "db_management/macros_for_manage_categories.html", "render_categories_table"
                )(cats)

    cats = Categories.query.all()

    return render_template("db_management/manage_categories.html", cats=cats)


@manage_db.route("/groupes", methods=["GET", "POST"])
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
                    "db_management/macros_for_manage_groupes.html", "render_prim_groupes_table"
                )(prim_groupes)

            if "new_sec_group" in req.keys():
                prim_g = req["new_sec_group"]["primary_group"]
                sec_g = req["new_sec_group"]["secondary_group"]

                new_s_g = SecondaryGroup(prim_title=prim_g, title=sec_g)

                db.session.add(new_s_g)
                db.session.commit()

                prim_groupes = PrimaryGroup.query.all()

                return get_template_attribute(
                    "db_management/macros_for_manage_groupes.html", "render_prim_groupes_table"
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
                    "db_management/macros_for_manage_groupes.html", "render_prim_groupes_table"
                )(prim_groupes)

            if "changes" in req.keys():
                changes = req["changes"]

                # TODO
                prim_groupes = PrimaryGroup.query.all()

                return get_template_attribute(
                    "db_management/macros_for_manage_groupes.html", "render_prim_groupes_table"
                )(prim_groupes)

    prim_groupes = PrimaryGroup.query.all()

    return render_template("db_management/manage_groupes.html", prim_groupes=prim_groupes)

@manage_db.route("/containers", methods=["GET", "POST"])
def edit_containers_db():
    if request.method == "POST":
        log.info(request.form)
        if request.data:  # check if request is json
            log.info(request.get_json())
            req = request.get_json()

            if "new_cont" in req.keys():
                try:
                    new_cont = Container(
                        stocks = req["new_cont"]['stocks'],
                        barcode = req["new_cont"]['barcode'],
                        current_location = req["new_cont"]['current_location'],
                        #target_location = req["new_cont"]['target_location'],
                        size = req["new_cont"]['size']
                    )

                    db.session.add(new_cont)
                    db.session.commit()
                except Exception as e:
                    flash("Error creating container")
            
            if "changes" in req.keys():
                # TODO: 
                flash("Not implemented")

                return get_template_attribute("db_management/macros_for_containers.html", "render_containers")(containers.query.limit(Config.QUERY_LIMIT_SOFT).all)
                

    containers = Container.query.limit(Config.QUERY_LIMIT_SOFT).all()

    return render_template("db_management/manage_containers.html", containers = containers)

@manage_db.route('/area', methods=['GET', 'POST'])
def edit_area_db():
    if request.method == "POST":
        if request.data:
            req = request.get_json()

            if "changes" in req.keys():
                log.info(req["changes"])

                changes = req["changes"]
                log.info(f"changes {type(changes)}: {changes}")
                for change in changes:
                    id = list(change.keys())[0]
                    logcb(f'id {type(id)}: {id}')
                    record = Area.query.get_or_404(int(id))
                    #log.info(f'record {type(record)}: {record}')

                    column_name = list(change[id].keys())[0]

                    if hasattr(record, column_name):
                        setattr(record, column_name, change[id][column_name])
                        log.info(f'record {type(record)}: {record}')

                        db.session.commit()
                    else:
                        log.info("No appropriate column found")

                areas = Area.query.all()
                return get_template_attribute("db_management/macros_for_manage_area.html", "render_areas")(areas)

    areas = Area.query.all()
    return render_template("db_management/manage_area.html", areas = areas)


@manage_db.route('/location', methods=['GET', 'POST'])
def edit_location_db():
    if request.method == "POST":
        if request.data:
            req = request.get_json()

            if "changes" in req.keys():
                log.info(req["changes"])

                changes = req["changes"]
                log.info(f"changes {type(changes)}: {changes}")
                for change in changes:
                    id = list(change.keys())[0]
                    logcb(f'id {type(id)}: {id}')
                    record = Location.query.get_or_404(int(id))
                    #log.info(f'record {type(record)}: {record}')

                    column_name = list(change[id].keys())[0]

                    if hasattr(record, column_name):
                        setattr(record, column_name, change[id][column_name])
                        log.info(f'record {type(record)}: {record}')

                        db.session.commit()
                    else:
                        log.info("No appropriate column found")

                locs = Location.query.all()
                return get_template_attribute("db_management/macros_for_manage_location.html", "render_locations")(locs)


    locs = Location.query.all()
    return render_template("db_management/manage_location.html", locations=locs)


