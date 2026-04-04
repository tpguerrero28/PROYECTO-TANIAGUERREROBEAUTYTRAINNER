from flask import Flask, render_template, request, redirect, flash

app = Flask(__name__)
app.secret_key = "beautytrainer2026"  # para flash

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