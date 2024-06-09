import os

class Config():

    prod = False

    if prod:
        
        AFSS_AREAS = [{"1" : 400}]

        QUERY_LIMIT_SOFT = 10
        SECRET_KEY = os.environ['FLASK_SECRET_KEY']
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', "webp"}
        UPLOAD_FOLDER = os.environ['UPLOAD_FOLDER']
        MYSQL_PASSWORD = os.environ["MYSQL_PASSWORD"]
        MYSQL_DB = os.environ['MYSQL_DB']
        MYSQL_USER = os.environ["MYSQL_USER"]
        MYSQL_PORT = os.environ['MYSQL_PORT']
        MYSQL_HOST = os.environ['MYSQL_HOST']
        SQLALCHEMY_DATABASE_URI = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
        CLIENT_SPS1_IP = "https://10.130.110.195"

    else:
        #import docker
        #client = docker.from_env()
        #client.containers.run('factory_db')
        #{area_number, belt_distance to L0 in mm}
        AFSS_AREAS = {"0": 0, "1" : 400, "2" : 600}
        AFSS_SHIFTER_POSITIONS = {"1": 250, "2": 255}
        QUERY_LIMIT_SOFT = 10
        SECRET_KEY = "f@ctory"
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', "webp"}
        UPLOAD_FOLDER_PROD_PIC = r"C:\Users\bsimb\HTL Mössingerstrasse\AFSS-automatic-factory-storage-system - General\Software\AFSS-Server\flask_pr\Prototyp_2\Static\product_pictures"
        UPLOAD_FOLDER = r"C:\Users\bsimb\HTL Mössingerstrasse\AFSS-automatic-factory-storage-system - General\Software\AFSS-Server\flask_pr\Prototyp_2\Static\images"
        MYSQL_PASSWORD = "factory"
        MYSQL_DB = "db_v1"
        MYSQL_USER = "root"
        MYSQL_PORT = "3308"
        MYSQL_HOST = "localhost"
        SQLALCHEMY_DATABASE_URI = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
        CLIENT_SPS1_IP = "http://192.168.0.55:5000"



    
