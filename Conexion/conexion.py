import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3309,               # <--- aquí el puerto correcto
        user="root",       # tu usuario MySQL
        password="12345",        # tu contraseña MySQL
        database="beauty_trainer"
    )