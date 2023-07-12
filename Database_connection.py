import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()


def database_connect():
    connection = mysql.connector.connect(host=os.getenv("DATABASE_HOST"), user=os.getenv("DATABASE_USER"),
                                         password=os.getenv("DATABASE_PASSWORD"),
                                         database=os.getenv("DATABASE_DATABASE"), auth_plugin="mysql_native_password")
    return connection
