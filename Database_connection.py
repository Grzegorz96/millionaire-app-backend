# Modules import.
import mysql.connector
import os
from dotenv import load_dotenv
# Load environment variables.
load_dotenv()


def database_connect():
    """The function responsible for creating database connection and returning it."""
    # Creating connection with database. Values are imported from environment variables.
    connection = mysql.connector.connect(host=os.getenv("DATABASE_HOST"), user=os.getenv("DATABASE_USER"),
                                         password=os.getenv("DATABASE_PASSWORD"),
                                         database=os.getenv("DATABASE_DATABASE"), auth_plugin="mysql_native_password")

    # Returning connection.
    return connection
