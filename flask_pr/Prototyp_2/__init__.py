from flask import Flask
from config import Config
from extensions import db, login_manager, bcrypt
from app import main
from wiki import wiki
from manage_db import manage_db
from afss_templates import afss_templates
from search_logic import search
from api import api
from tsets import testing
from dashboard import dashb


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
    app.register_blueprint(api, url_prefix='/api')    
    app.register_blueprint(testing, url_prefix='/test')    
    app.register_blueprint(dashb, url_prefix='/dashboard')    

    app.config['SECRET_KEY'] = 'f@ctory'
    app.config['SQLALCHEMY_RECORD_QUERIES'] = True

    if Config.prod:
        app.debug=os.environ['DEBUG']
    else:
        app.debug=True



    

    # Initialize SocketIO with the  
    # Flask app
    
    # Optional: Initialize login manager if required
    # login_manager.init_app(app)
    # login_manager.login_view = "login"

    return app

if __name__ == "__main__":
    app = create_app()
    

    if Config.prod:
        app.run(debug=os.environ['DEBUG'], host=os.environ['FLASK_RUN_HOST'], port=Config.PORT)
    else:
        app.run(debug=True, host="0.0.0.0", port=Config.PORT)
