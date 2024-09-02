from flask import Flask, request, render_template, redirect, url_for
import pandas as pd

app = Flask(__name__)

#Vincular Base de datos con este programa:
#Se le pide por favor que ingrese su dirección de archivo local para que funcione esté elemento.
ubicaciones = pd.read_csv('E:/Github/Primer-Proyecto-MYP/Proyecto Beta/HTML/static/Recursos/ubicaciones.csv')

@app.route('/')
def index():
    return render_template('Front.html')

@app.route('/procesar', methods=['POST'])
def procesar():
    origen = request.form['Parametro1']
    destino = request.form['Parametro2']

    filtroExacto = ubicaciones[(ubicaciones['origin'] == origen) & (ubicaciones['destination'] == destino)]

    if not filtroExacto.empty:
        primerElemento = filtroExacto.iloc[0]
        datos = {
            'origenLatitud': primerElemento['origin_latitude'],
            'origenLongitud': primerElemento['origin_longitude'],
            'destinoLatitud': primerElemento['destination_latitude'],
            'destinoLongitud': primerElemento['destination_longitude'],
            'origen': primerElemento['origin'],
            'destino': primerElemento['destination']
        }
    else:
        filtroOrigen = ubicaciones[ubicaciones['origin'] == origen]
        filtroDestino = ubicaciones[ubicaciones['destination'] == destino]

        datos = {
            'origenLatitud': filtroOrigen.iloc[0]['origin_latitude'] if not filtroOrigen.empty else "No disponoble",
            'origenLongitud': filtroOrigen.iloc[0]['origin_longitude'] if not filtroOrigen.empty else "No disponible",
            'destinoLatitud': filtroDestino.iloc[0]['destination_latitude'] if not filtroDestino.empty else "No disponible",
            'destinoLongitud': filtroDestino.iloc[0]['destination_longitude'] if not filtroDestino.empty else "No disponible",
            'origen': origen,
            'destino': destino
        }
    return redirect(url_for('resultado', **datos))

@app.route('/resultado')
def resultado():
    datos = request.args
    return render_template('Front2.html', datos = datos)

if __name__ == '__main__':
    app.run(debug = True)
