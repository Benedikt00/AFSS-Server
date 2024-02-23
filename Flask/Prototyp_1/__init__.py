from flask import Flask

from extensions import db, login_manager
from app import main
from flask_bcrypt import Bcrypt

def create_app(database_uri="sqlite:///db.sqlite3"):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:112358@localhost:3306/factory_db"
    app.config["SECRET_KEY"] = "f@ctory"

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(main)

    bcrypt = Bcrypt(app)

    login_manager.init_app(app)
    login_manager.login_view = "login"

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)