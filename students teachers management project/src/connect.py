import mysql.connector
from mysql.connector import Error
# for database connection
def create_connection(database=None):
    
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="",# username
            password="", # your DB password
            db = "" #your DB name
        )
        cursor = connection.cursor()
        if database:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
            connection.database = database
        print("connection success")
        return connection
    except Error as e:
        print("error", e)
        return None
