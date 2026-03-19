from flask import Flask, render_template, url_for, request, redirect, flash
from form import ProductoForm
from models import Producto, Inventario
from database import conectar_db, crear_tabla

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave-secreta'

# Inicializar inventario y base de datos
inventario = Inventario()
crear_tabla()

# =========================
# RUTAS PRINCIPALES
# =========================

@app.route('/')
def inicio():
    return render_template('Inicio.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/servicios')
def servicios():
    return render_template('servicios.html')


@app.route('/contacto')
def contacto():
    return render_template('contacto.html')


# =========================
# RUTA DE PRODUCTOS CON CRUD
# =========================

@app.route('/productos', methods=['GET', 'POST'])
def productos():
    form = ProductoForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        cantidad = form.cantidad.data
        precio = form.precio.data

        # Guardar en SQLite
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

    # Traer productos de SQLite
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos_db = cursor.fetchall()
    conn.close()
    # Actualizar inventario en memoria
    inventario.productos = {p[0]: Producto(*p) for p in productos_db}

    return render_template('inventario.html', productos=inventario.mostrar_todos(), form=form)


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
        producto = cursor.fetchone()
        conn.close()
        return render_template('actualizar_producto.html', producto=producto)


# =========================
# EJECUCIÓN
# =========================
if __name__ == '__main__':
    app.run(debug=True)
    