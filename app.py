from flask import Flask, render_template, request, redirect, url_for, flash
from Conexion.conexion import get_connection

app = Flask(__name__)
app.secret_key = "mi_clave_secreta"  # necesaria para flash

# ------------------ INICIO ------------------
@app.route("/")
def inicio():
    return render_template("inicio.html")

# ------------------ SERVICIOS ------------------
@app.route("/servicios")
def servicios():
    return render_template("servicios.html")

# ------------------ RESERVA ------------------
@app.route("/reserva", methods=["GET", "POST"])
def reserva():
    if request.method == "POST":
        nombre_cliente = request.form.get("nombre_cliente")
        telefono = request.form.get("telefono")
        servicio = request.form.get("servicio")
        fecha = request.form.get("fecha")
        hora = request.form.get("hora")

        if not nombre_cliente or not telefono or not servicio or not fecha or not hora:
            flash("Por favor completa todos los campos.", "danger")
            return redirect(url_for("reserva"))

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO reservas (nombre_cliente, telefono, servicio, fecha, hora)
                VALUES (%s, %s, %s, %s, %s)
            """, (nombre_cliente, telefono, servicio, fecha, hora))
            conn.commit()
            cursor.close()
            conn.close()
            flash("¡Reserva realizada con éxito!", "success")
            return redirect(url_for("reserva"))
        except Exception as e:
            flash(f"Error al conectar con la base de datos: {e}", "danger")
            return redirect(url_for("reserva"))

    return render_template("reserva.html")

# ------------------ VER RESERVAS ------------------
@app.route("/ver_reservas")
def ver_reservas():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reservas ORDER BY fecha, hora")
        reservas = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        flash(f"Error al obtener reservas: {e}", "danger")
        reservas = []

    return render_template("ver_reservas.html", reservas=reservas)

# ------------------ CONTACTO ------------------
@app.route("/contacto", methods=["GET", "POST"])
def contacto():
     # lógica para mostrar y enviar mensajes
    if request.method == "POST":
        nombre = request.form.get("nombre")
        email = request.form.get("email")
        mensaje = request.form.get("mensaje")

        if not nombre or not email or not mensaje:
            flash("Por favor completa todos los campos.", "danger")
            return redirect(url_for("contacto"))

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO contactos (nombre, email, mensaje)
                VALUES (%s, %s, %s)
            """, (nombre, email, mensaje))
            conn.commit()
            cursor.close()
            conn.close()
            flash("¡Mensaje enviado con éxito!", "success")
            return redirect(url_for("contacto"))
        except Exception as e:
            flash(f"Error al enviar el mensaje: {e}", "danger")
            return redirect(url_for("contacto"))

    return render_template("contacto.html")

# ------------------ MAIN ------------------
if __name__ == "__main__":
    app.run(debug=True)