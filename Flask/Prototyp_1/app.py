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
)
import json

from sql_connection_v2 import Database

import logging as log

from sqlalchemy import text, sql, select, exists
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
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError, NumberRange


from extensions import db as db_flask
from extensions import login_manager
from extensions import bcrypt
from models import Users, Cart, Parts

from configurations import config

from time import sleep

project_config = config("config.ini")

print(project_config.get_option('Settings','max_num_boxes'))


fr_db = Database("mysql://root:112358@localhost:3306/test_db_bauteile", "db_factory_p1")



# db_flask = SQLAlchemy(app)


main = Blueprint("main", __name__)

@login_manager.user_loader
def load_user(name):
    return Users.query.get(name)


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


@main.route("/")
def root():
    # Redirect to "/sectionb"
    # return redirect(url_for('selection'))
    return render_template("index.html")


all_keys_for_search = fr_db.get_first_identifiers()


def get_highest_or_default__cart():
    # Check if there is any data in the User table
    if db_flask.session.query(Cart).count() == 0:
        # No data, return a default value
        return 0
    else:
        # Data exists, return the highest value in the 'age' column
        highest = db_flask.session.query(db_flask.func.max(Cart.id_sort)).scalar()
        return highest


def check_if_part_exists(part_id):
    exists_query = db_flask.session.query(
        db_flask.exists().where(Cart.part_id == part_id)
    )
    element_exists = exists_query.scalar()
    return element_exists


@main.route("/selection", methods=["get", "post"])
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

        # handle request for order
        if "add_to_cart" in data.keys():

            c_order = json.loads(data["add_to_cart"])

            part_id_to_check = int(c_order["id"])

            element_exists = check_if_part_exists(part_id_to_check)
            if not element_exists:
                log.info("new")
                sort_id = get_highest_or_default__cart() + 1

                new_entry = Cart(
                    id_sort=sort_id,
                    part_id=int(c_order["id"]),
                    quantity=int(c_order["quantity"]),
                )
                db_flask.session.add(new_entry)
                db_flask.session.commit()
            else:
                # Update the column by adding the specified value
                row = Cart.query.filter_by(part_id=part_id_to_check).first()
                row.quantity += c_order["quantity"]
                db_flask.session.commit()
            
            return "200"



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


@main.route("/manage_db", methods=["get", "post"])
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


@main.route("/manage_db/<id>", methods=["get", "post"])
def edit_db(id):
    if request.method == "POST":
        data = request.form.to_dict()

        if "change_db_entry" in data.keys():
            print(data["change_db_entry"])
            inp = json.loads(data["change_db_entry"])
            rep = fr_db.edit_db_entry_after_cat(
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


@main.route("/new_entry", methods=["get", "post"])
def new_entry():
    if request.method == "POST":
        data = request.form.to_dict()
        log.info(f"data new entry post {type(data)}: {data}")

    return render_template("new_entry.html")


@main.route("/new_entry/afss", methods=["get", "post"])
def new_entry_afss():
    if request.method == "POST":
        data = request.form.to_dict()
        log.info(f"data new entry post {type(data)}: {data}")

    return render_template("storage_possibilities/afss.html")


class LoginForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Username"},
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Password"},
    )

    submit = SubmitField("Login")


@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(
                user.password_hash.encode("utf8"), form.password.data
            ):

                login_user(user)
                session["access"] = user.access
                return redirect(url_for("main.root"))
    return render_template("login.html", form=form)


class RegisterForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Username"},
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Password"},
    )

    access = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "0"})

    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = Users.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                "That username already exists. Please choose a different one."
            )


@main.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf8"
        )
        new_user = Users(
            username=form.username.data,
            password_hash=hashed_password,
            access=form.access.data,
        )
        db_flask.session.add(new_user)
        db_flask.session.commit()
        return redirect(url_for("login"))

    return render_template("register.html", form=form)

@main.route('/logout')
@login_required
def logout():
    session.pop('access', None)
    return redirect(url_for('main.root'))

def load_cart_data():
    cart_data = Cart.query.all()
    result = []

    for cart_item in cart_data:
        result.append(
            {
                "id": cart_item.id,
                "id_sort": cart_item.id_sort,
                "part_id": cart_item.part_id,
                "quantity": cart_item.quantity,
                # Include other fields as needed
            }
        )

    return sorted(result, key=lambda x: x["id_sort"])

def add_orders_to_stack(max_out):
    pass

def move_element_with_new_id_sort(part_id_param: int, new_id_sort: int):
    """moves an element to a new position, updates the indeces of the oder elements
    
    Keyword arguments:
    part_id_param -- id the id of the part of which the order beeing changed
    new_id_sort -- position where the element shoult go to
    Return: none
    """
    
    orig_id_sort = Cart.query.filter_by(id = part_id_param).first().id_sort
    
    diff = new_id_sort - orig_id_sort
    log.info(f'diff {type(diff)}: {diff}')

    if diff > 0:
        log.info("pos")
        Cart.query.filter(Cart.id_sort == orig_id_sort).update({Cart.id_sort: (-1)})
        Cart.query.filter(Cart.id_sort.between(orig_id_sort, new_id_sort)).\
                update({Cart.id_sort: Cart.id_sort - 1}, synchronize_session=False)
        Cart.query.filter(Cart.id_sort == -1).update({Cart.id_sort: new_id_sort})
    
    if diff < 0:
        log.info("neg")
        Cart.query.filter(Cart.id_sort == orig_id_sort).update({Cart.id_sort: (-1)})
        Cart.query.filter(Cart.id_sort.between(new_id_sort, orig_id_sort)).\
                update({Cart.id_sort: Cart.id_sort + 1}, synchronize_session=False)
        Cart.query.filter(Cart.id_sort == -1).update({Cart.id_sort: new_id_sort})
    
    db_flask.session.commit()


def reset_cart_and_autoincrement():
    # Function to delete all data from the Cart table and reset the auto-increment counter
    db_flask.session.query(Cart).delete()
    db_flask.session.execute(text("ALTER TABLE cart AUTO_INCREMENT = 0"))
    db_flask.session.commit()

def change_quantity(id, new_val):
    Cart.query.filter(Cart.id == id).update({Cart.quantity: new_val})
    db_flask.session.commit()

def delete_item(id):
    element_to_delete = Cart.query.get(id)
    if element_to_delete:
            beg_sort_id = element_to_delete.id_sort
            db_flask.session.delete(element_to_delete)
            Cart.query.filter(Cart.id_sort > beg_sort_id).\
                update({Cart.id_sort: Cart.id_sort - 1})
            
            db_flask.session.commit()

class OrderSubmitFiled(FlaskForm):
    num_box_max = IntegerField('num_max_box', validators=[
        NumberRange(min=1, max=project_config.get_option('Settings','max_num_boxes'), message='Value must be between 0 and 100')
    ], default=5)
    submit_button = SubmitField('Submit')

@main.route("/cart", methods=["GET", "POST"])
def cart():
    form = OrderSubmitFiled()
    if request.method == "POST":

        data = request.form.to_dict()
        if "change_cart" in data.keys():
            part_id = json.loads(data["change_cart"])["id"]
            new_index = json.loads(data["change_cart"])["new_index"]
            log.info(f"cart {type(data)}: {data}, {part_id} , {new_index}")
            move_element_with_new_id_sort(part_id, new_index)
        
        if "reset_cart" in data.keys():
            log.info("resetting cart")
            reset_cart_and_autoincrement()

        if "change_quant" in data.keys():
            id = json.loads(data["change_quant"])["id"]
            new_val = json.loads(data["change_quant"])["new_quant"]
            change_quantity(id, new_val)
        
        if "delete_item" in data.keys():
            id = json.loads(data["delete_item"])["id"]
            delete_item(id)

        if form.validate_on_submit():
            max_out = form.num_box_max.data
            add_orders_to_stack(max_out)

        data = load_cart_data()

        return render_template("cart_table.html", data=data)

    data = load_cart_data()
    return render_template("cart.html", data=data, OrderSubmitFiled = form)


@main.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@main.route("/test")
def test():
    return render_template("test.html")


if __name__ == "__main__":
    import __init__

    __init__.create_app()
