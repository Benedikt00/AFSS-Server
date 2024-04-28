from flask import Flask
from config import Config
from extensions import db, login_manager, bcrypt
from app import main
from wiki import wiki
from manage_db import manage_db
from afss_templates import afss_templates
from search_logic import search

import os

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="Static")    
    app.config.from_object(Config)

    db.init_app(app)

    bcrypt.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(wiki, url_prefix='/wiki')    
    app.register_blueprint(search, url_prefix='/search')    
    app.register_blueprint(afss_templates, url_prefix='/afss_templates')    
    app.register_blueprint(manage_db, url_prefix='/manage_db')    
    
    app.app_context()
    #login_manager.init_app(app)
    #login_manager.init_app(app)
    #login_manager.login_view = "login"
    

    return app

if __name__ == "__main__":
    app = create_app()
    if Config.prod:
        app.run(debug=os.environ['DEBUG'], host=os.environ['FLASK_RUN_HOST'], port=5000)
    else:
        app.run(debug=True, host="0.0.0.0", port=5000)
