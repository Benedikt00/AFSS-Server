import os

class Config():

    prod = False

        #id, distance from L0
    AFSS_AREAS = {"0": 0, "1" : 400, "2" : 600}
    AFSS_SHIFTER_POSITIONS = {"1": 250, "2": 255}
    QUERY_LIMIT_SOFT = 10
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', "webp"}


    if prod:
        import socket
        hostname = socket.gethostname()
        IP_ADDR = socket.gethostbyname(hostname)

        PORT = os.environ(['PORT'])
        DOMAIN = f"{IP_ADDR}:{PORT}/"


        QUERY_LIMIT_SOFT = 10
        SECRET_KEY = os.environ['FLASK_SECRET_KEY']
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', "webp"}
        UPLOAD_FOLDER = os.environ['UPLOAD_FOLDER']
        UPLOAD_FOLDER_PROD_PIC = os.environ['UPLOAD_FOLDER_PROD_PIC']


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
        import socket
        hostname = socket.gethostname()
        
        IP_ADDR = socket.gethostbyname(hostname)
        PORT = 5000
        DOMAIN = f"{IP_ADDR}:{PORT}/"

        SECRET_KEY = "f@ctory"
        
        UPLOAD_FOLDER_PROD_PIC = r"C:\Users\bsimb\HTL Mössingerstrasse\AFSS-DA - Dokumente\Software\AFSS-Server\flask_pr\Prototyp_2\Static\product_pictures"
        UPLOAD_FOLDER = r"C:\Users\bsimb\HTL Mössingerstrasse\AFSS-DA - Dokumente\Software\AFSS-Server\flask_pr\Prototyp_2\Static\images"
        MYSQL_PASSWORD = "factory"
        MYSQL_DB = "db_v1"
        MYSQL_USER = "root"
        MYSQL_PORT = "3308"
        MYSQL_HOST = "localhost"
        SQLALCHEMY_DATABASE_URI = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

        CLIENT_SPS1_IP = f"http://{IP_ADDR}:5001"




