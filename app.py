from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/reserva/<cliente>')
def reserva(cliente):
    return f'Bienvenida {cliente}, tu reserva fue registrada.'

@app.route('/servicio/<nombre>')
def servicio(nombre):
    return f'Servicio: {nombre}'

if __name__ == '__main__':
    app.run(debug=True)