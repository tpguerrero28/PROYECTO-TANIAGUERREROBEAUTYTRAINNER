import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            port=3309,
            user="root",
            password="12345",
            database="beauty_trainer"
        )
        return connection
    except Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None