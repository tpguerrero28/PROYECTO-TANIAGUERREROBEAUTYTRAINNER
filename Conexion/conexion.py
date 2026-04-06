import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            port=3309,          # Puerto que me dijiste
            user="root",        # Usuario
            password="12345",   # Tu contraseña
            database="beauty_trainer"  # Nombre de tu base de datos
        )
        return connection
    except Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None