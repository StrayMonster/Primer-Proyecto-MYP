from flask import Flask, request, render_template, redirect, url_for
import pandas as pd

app =  Flask(__name__)

@app.route('/')
def formulario():
    return render_template('formulario.html')

@app.route('/procesar', methods=['POST'])
def procesar():
    origenForm = request.form['Parametro1']
    destinoForm = request.form['Parametro2']

    #Vincular Base de datos con este programa:
    #Se le pide por favor que ingrese su dirección de archivo local para que funcione esté elemento.
    ubicaciones = pd.read_csv('E:/Github/Primer-Proyecto-MYP/Proyecto Beta/HTML/Recursos/ubicaciones.csv')
    print(ubicaciones.head())

    filtroReal = ubicaciones[(ubicaciones['origin'] == 'MEX') & (ubicaciones['destination'] == 'MTY')]

    if not filtroReal.empty:
        primerElemento = filtroReal.iloc[0]
        origenLatitud = primerElemento['origin_latitude']
        origenLongitud = primerElemento['origin_longitude']
        destinoLatitud = primerElemento['destination_latitude']
        destinoLongitud = primerElemento['destination_longitude']
        origen = primerElemento['origin']
        destino = primerElemento['destination']
    filtroReal.to_csv('HTML/Recursos/resultado.csv', index = False)
    return redirect(url_for('resultado'))

@app.route('/resultado')
def resultado():
    ubicacionesH = pd.read_csv('E:/Github/Primer-Proyecto-MYP/Proyecto Beta/HTML/Recursos/ubicaciones.csv') 
    tablaHtml = ubicacionesH.to_html()
    return render_template('Front2.html', tabla = tablaHtml)

if __name__ == '__main__':
    app.run(debug = True)

