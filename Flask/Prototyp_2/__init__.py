from flask import Flask
from config import Config
from extensions import db, login_manager, bcrypt
from app import main

import os

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="Static")    
    app.config.from_object(Config)

    db.init_app(app)

    bcrypt.init_app(app)
    app.register_blueprint(main)    
    app.app_context()
    #login_manager.init_app(app)
    #login_manager.init_app(app)
    #login_manager.login_view = "login"
    

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=os.environ['DEBUG'], host=os.environ['FLASK_RUN_HOST'], port=5000)
    