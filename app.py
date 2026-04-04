from flask import Flask, render_template, request, redirect, url_for
from Conexion.conexion import get_connection

app = Flask(__name__)

@app.route('/reserva', methods=['GET', 'POST'])
def reserva():
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        servicio = request.form['servicio']
        fecha = request.form['fecha']
        hora = request.form['hora']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO reservas (nombre_cliente, telefono, servicio, fecha, hora) VALUES (%s, %s, %s, %s, %s)",
                       (nombre, telefono, servicio, fecha, hora))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('reserva_exitosa'))
    
    return render_template('reserva.html')

@app.route('/reserva_exitosa')
def reserva_exitosa():
    return "¡Reserva registrada con éxito!"

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/productos')
def productos():
    return render_template('productos.html')

@app.route('/producto_form', methods=['GET', 'POST'])
def producto_form():
    if request.method == 'POST':
        flash("Producto agregado (simulado)", "success")  # aún no trabajamos con BD
        return redirect('/productos')
    return render_template('producto_form.html')

@app.route('/datos')
def datos():
    return render_template('datos.html')

@app.route('/contactos', methods=['GET', 'POST'])
def contactos():
    if request.method == 'POST':
        flash("¡Formulario enviado! (simulado)", "success")
        return redirect('/contactos')
    return render_template('contactos.html')

if __name__ == '__main__':
    app.run(debug=True)