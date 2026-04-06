from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from fpdf import FPDF

from conexion import init_app, mysql
from services.producto_service import crear_producto, listar_productos, obtener_producto, actualizar_producto, eliminar_producto
from models.usuario import Usuario
from forms.producto_form import ProductoForm



# -------------------- APP --------------------
app = Flask(__name__)
app.secret_key = "clave_secreta"

# Inicializar conexión
mysql.init_app(app) # activa la conexión con MySQL

# -------------------- MYSQL --------------------
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3309
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'beauty_trainer'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# -------------------- LOGIN --------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (user_id,))
    data = cursor.fetchone()
    cursor.close()
    if data:
        return Usuario(data["id_usuario"], data["nombre"], data["email"], data["password"])
    return None

# -------------------- RUTAS GENERALES --------------------
@app.route("/")
def inicio():
    return render_template("inicio.html")


# -------------------- USUARIOS --------------------
@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        mensaje = request.form["mensaje"]

        # Guardar en la base de datos
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO contactos (nombre, email, mensaje) VALUES (%s, %s, %s)",
            (nombre, email, mensaje)
        )
        mysql.connection.commit()
        cursor.close()

        flash("Tu mensaje ha sido enviado con éxito", "success")
        return redirect(url_for("contacto"))

    return render_template("contacto.html")

@app.route("/servicios")
def servicios():
    return render_template("servicios.html")

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form['nombre']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
                       (nombre, email, password))
        mysql.connection.commit()
        cursor.close()

        flash("Usuario registrado correctamente", "success")
        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user['password'], password):
            usuario = Usuario(user['id_usuario'], user['nombre'], user['email'], user['password'])
            login_user(usuario)
            return redirect(url_for('inicio'))
        else:
            flash("Correo o contraseña incorrectos", "danger")
    return render_template('login.html')

@app.route("/reserva", methods=["GET", "POST"])
def reserva():
    if request.method == "POST":
        nombre = request.form["nombre_cliente"]
        telefono = request.form["telefono"]
        servicio = request.form["servicio"]
        fecha = request.form["fecha"]
        hora = request.form["hora"]

        # Guardar en la base de datos
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO reservas (nombre_cliente, telefono, servicio, fecha, hora) VALUES (%s, %s, %s, %s, %s)",
            (nombre, telefono, servicio, fecha, hora)
        )
        mysql.connection.commit()
        cursor.close()

        flash("Reserva creada con éxito", "success")
        return redirect(url_for("reserva"))

    return render_template("reserva.html")

@app.route("/ver_reservas")
def ver_reservas():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM reservas ORDER BY fecha, hora")
    reservas = cursor.fetchall()
    cursor.close()
    return render_template("ver_reservas.html", reservas=reservas)

@app.route("/editar_reserva/<int:id>", methods=["GET", "POST"])
def editar_reserva(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM reservas WHERE id_reserva = %s", (id,))
    reserva = cursor.fetchone()

    if request.method == "POST":
        nombre = request.form["nombre_cliente"]
        telefono = request.form["telefono"]
        servicio = request.form["servicio"]
        fecha = request.form["fecha"]
        hora = request.form["hora"]

        cursor.execute("""
            UPDATE reservas
            SET nombre_cliente=%s, telefono=%s, servicio=%s, fecha=%s, hora=%s
            WHERE id_reserva=%s
        """, (nombre, telefono, servicio, fecha, hora, id))
        mysql.connection.commit()
        cursor.close()

        flash("Reserva actualizada con éxito", "success")
        return redirect(url_for("ver_reservas"))

    cursor.close()
    return render_template("editar_reserva.html", reserva=reserva)


@app.route("/eliminar_reserva/<int:id>", methods=["POST"])
def eliminar_reserva(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM reservas WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()

    flash("Reserva eliminada con éxito", "danger")
    return redirect(url_for("ver_reservas"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada", "info")
    return redirect(url_for('login'))

# -------------------- PRODUCTOS --------------------
@app.route("/productos")
@login_required
def productos():
    productos = listar_productos()
    return render_template("productos/listar.html", productos=productos)

@app.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        crear_producto(form.nombre.data, form.precio.data, form.stock.data)
        flash("Producto agregado", "success")
        return redirect(url_for('productos'))
    return render_template("productos/nuevo.html", form=form)

@app.route("/productos/editar/<int:id_producto>", methods=["GET", "POST"])
@login_required
def editar_producto(id_producto):
    producto = obtener_producto(id_producto)
    if not producto:
        flash("Producto no encontrado", "danger")
        return redirect(url_for('productos'))

    form = ProductoForm(data=producto)
    if form.validate_on_submit():
        actualizar_producto(id_producto, form.nombre.data, form.precio.data, form.stock.data)
        flash("Producto actualizado", "success")
        return redirect(url_for('productos'))

    return render_template("productos/editar.html", form=form, producto=producto)

@app.route("/productos/eliminar/<int:id_producto>", methods=["POST"])
@login_required
def eliminar_producto_ruta(id_producto):
    eliminar_producto(id_producto)
    flash("Producto eliminado", "info")
    return redirect(url_for('productos'))

# -------------------- PDF PRODUCTOS --------------------
@app.route("/reporte_reservas")
def reporte_reservas():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM reservas ORDER BY fecha, hora")
    reservas = cursor.fetchall()
    cursor.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Reporte de Reservas", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", 'B', 10)
    pdf.cell(15, 10, "ID", 1)
    pdf.cell(40, 10, "Nombre", 1)
    pdf.cell(30, 10, "Teléfono", 1)
    pdf.cell(50, 10, "Servicio", 1)
    pdf.cell(30, 10, "Fecha", 1)
    pdf.cell(20, 10, "Hora", 1)
    pdf.ln()

    pdf.set_font("Arial", size=10)
    for r in reservas:
        pdf.cell(15, 10, str(r["id_reserva"]), 1)
        pdf.cell(40, 10, r["nombre_cliente"], 1)
        pdf.cell(30, 10, r["telefono"] if r["telefono"] else "-", 1)
        pdf.cell(50, 10, r["servicio"], 1)
        pdf.cell(30, 10, str(r["fecha"]), 1)
        pdf.cell(20, 10, str(r["hora"]), 1)
        pdf.ln()

    pdf.output("reservas.pdf")
    return send_file("reservas.pdf", as_attachment=True)

# -------------------- RUN --------------------
if __name__ == "__main__":
    app.run(debug=True)