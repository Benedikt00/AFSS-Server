
import os

class Config():
    SECRET_KEY = os.environ['FLASK_SECRET_KEY']
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', "webp"}
    UPLOAD_FOLDER = os.environ['UPLOAD_FOLDER']
    MYSQL_PASSWORD = os.environ["MYSQL_PASSWORD"]
    MYSQL_DB = os.environ['MYSQL_DB']
    MYSQL_USER = os.environ["MYSQL_USER"]
    MYSQL_PORT = os.environ['MYSQL_PORT']
    MYSQL_HOST = os.environ['MYSQL_HOST']
    SQLALCHEMY_DATABASE_URI = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"