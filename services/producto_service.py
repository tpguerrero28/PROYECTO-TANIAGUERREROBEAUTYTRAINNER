from conexion import mysql

def crear_producto(nombre, precio, stock):
    cursor = mysql.connection.cursor()
    query = "INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)"
    cursor.execute(query, (nombre, precio, stock))
    mysql.connection.commit()
    cursor.close()

def listar_productos():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    cursor.close()
    return productos

def obtener_producto(id_producto):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM productos WHERE id_producto = %s"
    cursor.execute(query, (id_producto,))
    producto = cursor.fetchone()
    cursor.close()
    return producto

def actualizar_producto(id_producto, nombre, precio, stock):
    cursor = mysql.connection.cursor()
    query = "UPDATE productos SET nombre = %s, precio = %s, stock = %s WHERE id_producto = %s"
    cursor.execute(query, (nombre, precio, stock, id_producto))
    mysql.connection.commit()
    cursor.close()

def eliminar_producto(id_producto):
    cursor = mysql.connection.cursor()
    query = "DELETE FROM productos WHERE id_producto = %s"
    cursor.execute(query, (id_producto,))
    mysql.connection.commit()
    cursor.close()