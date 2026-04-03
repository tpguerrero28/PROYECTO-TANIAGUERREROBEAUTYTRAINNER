import sqlite3

DB_FILE = 'inventario.db'

def conectar_db():
    """Conecta a la base de datos SQLite"""
    return sqlite3.connect(DB_FILE)

def crear_tabla():
    """Crea la tabla productos si no existe"""
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()