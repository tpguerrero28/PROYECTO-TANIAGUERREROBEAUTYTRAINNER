from flask import Flask, render_template, url_for, request, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField
from wtforms.validators import DataRequired, NumberRange
import sqlite3
import os

# =========================
# CONFIGURACIÓN DE LA APP
# =========================
app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave-secreta'

# =========================
# FORMULARIO DE PRODUCTOS
# =========================
class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired(), NumberRange(min=0)])
    precio = DecimalField('Precio', validators=[DataRequired(), NumberRange(min=0)])

# =========================
# BASE DE DATOS
# =========================
DB_PATH = 'productos.db'

def conectar_db():
    return sqlite3.connect(DB_PATH)

def crear_tabla():
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

# Crear la tabla al iniciar
crear_tabla()

# =========================
# RUTAS PRINCIPALES
# =========================
@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/servicio_detalle/<int:id_servicio>')
def servicio_detalle(id_servicio):
    # Aquí podrías obtener información de un servicio específico si tuvieras DB de servicios
    return render_template('servicio_detalle.html', id_servicio=id_servicio)

@app.route('/reserva')
def reserva():
    return render_template('reserva.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

# =========================
# CRUD PRODUCTOS
# =========================
@app.route('/productos', methods=['GET', 'POST'])
def productos():
    form = ProductoForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        cantidad = form.cantidad.data
        precio = float(form.precio.data)

        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)",
            (nombre, cantidad, precio)
        )
        conn.commit()
        conn.close()
        flash('Producto agregado con éxito!', 'success')
        return redirect(url_for('productos'))

    # Obtener productos
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos_db = cursor.fetchall()
    conn.close()

    productos = [{"id": p[0], "nombre": p[1], "cantidad": p[2], "precio": p[3]} for p in productos_db]

    return render_template('productos.html', productos=productos, form=form)

@app.route('/eliminar_producto/<int:id_producto>')
def eliminar_producto(id_producto):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id=?", (id_producto,))
    conn.commit()
    conn.close()
    flash('Producto eliminado!', 'warning')
    return redirect(url_for('productos'))

@app.route('/actualizar_producto/<int:id_producto>', methods=['GET', 'POST'])
def actualizar_producto(id_producto):
    conn = conectar_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])
        cursor.execute(
            "UPDATE productos SET nombre=?, cantidad=?, precio=? WHERE id=?",
            (nombre, cantidad, precio, id_producto)
        )
        conn.commit()
        conn.close()
        flash('Producto actualizado!', 'success')
        return redirect(url_for('productos'))
    else:
        cursor.execute("SELECT * FROM productos WHERE id=?", (id_producto,))
        p = cursor.fetchone()
        producto = {"id": p[0], "nombre": p[1], "cantidad": p[2], "precio": p[3]} if p else None
        conn.close()
        return render_template('actualizar_producto.html', producto=producto)

# =========================
# EJECUCIÓN
# =========================
if __name__ == '__main__':
    app.run(debug=True)
    