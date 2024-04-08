class Config():
    SECRET_KEY = "f@ctory"
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', "webp"}
    UPLOAD_FOLDER = "Static/product_pictures"
    SQLALCHEMY_DATABASE_URI = "mysql://root:factory@localhost:3308/db_v1"