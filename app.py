from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import Usuario
from flask_mysqldb import MySQL

app = Flask(__name__)

# clave
app.secret_key = "clave_secreta"

# config MYSQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3309
app.config['MYSQL_USER'] = 'tania'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'beauty_trainer'  # tu base de datos

# CONEXIÓN
mysql = MySQL(app)

# LOGIN CONFIG
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (user_id,))
    user = cursor.fetchone()

    if user:
        return Usuario(user[0], user[1], user[2], user[3])
    return None

# ------------------ RUTAS ------------------

@app.route("/")
def inicio():
    return render_template("inicio.html")


@app.route("/servicios")
def servicios():
    return render_template("servicios.html")


# CONTACTO
@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        mensaje = request.form["mensaje"]

        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO contactos (nombre, email, mensaje) VALUES (%s, %s, %s)",
            (nombre, email, mensaje)
        )
        mysql.connection.commit()
        cursor.close()

        flash("Mensaje enviado correctamente", "success")
        return redirect(url_for("contacto"))

    return render_template("contacto.html")


# RESERVA (PROTEGIDA)
@app.route("/reserva", methods=["GET", "POST"])
@login_required
def reserva():
    if request.method == "POST":
        nombre_cliente = request.form["nombre_cliente"]
        servicio = request.form["servicio"]
        fecha = request.form["fecha"]
        hora = request.form["hora"]

        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO reservas (nombre_cliente, servicio, fecha, hora)
            VALUES (%s, %s, %s, %s)
        """, (nombre_cliente, servicio, fecha, hora))

        mysql.connection.commit()
        cursor.close()

        flash("Reserva realizada con éxito", "success")
        return redirect(url_for("reserva"))

    return render_template("reserva.html")


@app.route("/ver_reservas")
@login_required
def ver_reservas():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM reservas")
    reservas = cursor.fetchall()
    cursor.close()

    return render_template("ver_reservas.html", reservas=reservas)


# REGISTRO
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
            (nombre, email, password)
        )
        mysql.connection.commit()
        cursor.close()

        flash("Usuario registrado correctamente", "success")
        return redirect(url_for('login'))
    
    return render_template('registro.html')


# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user[3], password):
            usuario = Usuario(user[0], user[1], user[2], user[3])
            login_user(usuario)

            flash("Bienvenido", "success")
            return redirect(url_for('inicio'))
        else:
            flash("Correo o contraseña incorrectos", "danger")

    return render_template('login.html')


# LOGOUT
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada", "info")
    return redirect(url_for('login'))


# RUN
if __name__ == "__main__":
    app.run(debug=True)
