#Se importan los elementos que se van a usar, flask, pandas y la api.
from flask import Flask, request, render_template, redirect, url_for, session
import pandas as pd
import requests
import os

app = Flask(__name__)
app.secret_key = 'waos'

#Vincular Base de datos con este programa:
#Se le pide por favor que ingrese su dirección de archivo local para que funcione esté elemento.
ubicaciones = pd.read_csv('E:/Github/Primer-Proyecto-MYP/Proyecto Beta/HTML/static/Recursos/ubicaciones.csv')

API_KEY = '644a995fb441ee0ec22ae8ff3865161f'

cache_clima = {}

def obtener_clima(latitud, longitud):
    clave_cache = f"{latitud},{longitud}"
    if clave_cache in cache_clima:
        return cache_clima[clave_cache]
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitud}&lon={longitud}&appid={API_KEY}&units=metric"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        datos_clima = respuesta.json()
        clima = {
            'temperatura': datos_clima['main']['temp'],
            'sensacion_termica': datos_clima['main']['feels_like'],
            'humedad': datos_clima['main']['humidity'],
            'descripcion': datos_clima['weather'][0]['description'],
            'icono':datos_clima['weather'][0]['icon']
        }
        cache_clima[clave_cache] = clima
        return clima
    else:
        return None

def seleccionarGif(descripcion):
    descripcion = descripcion.lower().strip()
    gifs = {
        'thunderstorm with light rain': 'LluviaElectrica.gif',
        'thunderstorm with rain': 'LluviaElectrica.gif',
        'thunderstorm with heavy rain': 'LluviaElectrica.gif',
        'light thunderstorm': 'LluviaElectrica.gif',
        'thunderstorm': 'LluviaElectrica.gif',
        'heavy thunderstorm': 'LluviaElectrica.gif',
        'ragged thunderstorm': 'LluviaElectrica.gif',
        'thunderstorm with light drizzle': 'LluviaElectrica.gif',
        'thunderstorm with drizzle': 'LluviaElectrica.gif',
        'thunderstorm with heavy drizzle': 'LluviaElectrica.gif',

        'light intensity drizzle': 'LluviaLL.gif',
        'drizzle': 'LluviaL.gif',
        'heavy intensity drizzle': 'LluviaL.gif',
        'light intensity drizzle rain': 'LluviaLL.gif',
        'drizzle rain': 'LluviaL.gif',
        'heavy intensity drizzle rain': 'LluviaL.gif',
        'shower rain and drizzle': 'LluviaL.gif',
        'heavy shower rain and drizzle': 'LluviaL.gif',        
        'shower drizzle': 'LluviaL.gif',

        'light rain': 'LluviaLL.gif',
        'moderate rain': 'LluviaM.gif',
        'heavy intensity rain': 'LluviaH.gif',
        'very heavy rain': 'LluviaH.gif',
        'extreme rain': 'LluviaH.gif',
        'freezing rain': 'AguaNieve.gif',
        'light intensity shower rain': 'LluviaH.gif',
        'shower rain': 'LluviaH.gif',
        'heavy intensity shower rain': 'LluviaH.gif',
        'ragged shower rain': 'LluviaH.gif',

        'light snow': 'NevandoL.gif',
        'Snow': 'NevandoL.gif',
        'Heavy snow': 'Nevando.gif',
        'Sleet': 'AguaNieve.gif',
        'Light shower sleet': 'AguaNieve.gif',
        'Shower sleet': 'AguaNieve.gif',
        'Light rain and snow': 'Nevando.gif',
        'Rain and snow': 'Nevando.gif',
        'Light shower snow': 'Nevando.gif',
        'Shower snow': 'Nevando.gif',
        'Heavy shower snow': 'Nevando.gif',

        'mist': 'Neblina.gif',
        'smoke': 'Neblina.gif',
        'haze': 'Neblina.gif',
        'sand': 'Arena.gif',
        'dust whirls': 'Arena.gif',
        'fog': 'Neblina.gif',
        'dust': 'Neblina.gif',
        'volcanic ash': 'Ceniza.gif',
        'squalls': 'AguaNieve.gif',
        'tornado': 'Tornado.gif',

        'clear sky': 'Despejado.jpg',
    }

    base_path = '/Recursos/Imagenes/'

    print(f"Descripción recibida: {descripcion}")
    for key, gif in gifs.items():
        if key in descripcion:
            gif_path = os.path.join(base_path, gif)
            full_gif_path = os.path.join('static', gif_path)
            print(f"Ruta del Gif: {gif_path}")
            print(f"Ruta completa del gif: {full_gif_path}")
            if os.path.exists(full_gif_path):
                print(f"Después de verificar que exitse: {full_gif_path}")
                return gif_path
            else:
                print(f"GIF no encontrado: {full_gif_path}, asignando Deafult")
                return os.path.join(base_path, 'Default.gif')
    print("Descripcion no coincide, asignando Default")
    return os.path.join(base_path, 'Default.gif')
            

#Se declara la ruta de inicio.
@app.route('/')
def index():
    return render_template('Front.html')

#Se declará los elementos que se van a procesar, en este caso buscar en el csv los parametros otorgados en el front.html
@app.route('/procesar', methods=['POST'])
def procesar():
    #Variables que almacenan las respuestas del forms de front.html, en este caso como el nombre de las variables indica.
    origen = request.form['Parametro1']
    destino = request.form['Parametro2']

    #Filtro que busca en csv, la fila en la que ambos parametros son iguales, esto facilita la busqueda y la obtención de datos posteriores.
    filtroExacto = ubicaciones[(ubicaciones['origin'] == origen) & (ubicaciones['destination'] == destino)]

    #Si dicho filtro no es vació, entonces procesa los datos de csv en variables.
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
    # En otro caso, si no existe una fila en la que el origen y el destino coincide, busca por separado en cada columna, hasta que se encuentre dicho elemento.
    else:
        filtroOrigen = ubicaciones[ubicaciones['origin'] == origen]
        filtroDestino = ubicaciones[ubicaciones['destination'] == destino]

        datos = {
            'origenLatitud': filtroOrigen.iloc[0]['origin_latitude'] if not filtroOrigen.empty else "No disponible",
            'origenLongitud': filtroOrigen.iloc[0]['origin_longitude'] if not filtroOrigen.empty else "No disponible",
            'destinoLatitud': filtroDestino.iloc[0]['destination_latitude'] if not filtroDestino.empty else "No disponible",
            'destinoLongitud': filtroDestino.iloc[0]['destination_longitude'] if not filtroDestino.empty else "No disponible",
            'origen': origen,
            'destino': destino
        }
    clima_origen = obtener_clima(datos['origenLatitud'], datos['origenLongitud'])
    clima_destino = obtener_clima(datos['destinoLatitud'], datos['destinoLongitud'])

    
    datos['clima_origen'] = clima_origen
    datos['gif_origen'] = seleccionarGif(clima_origen['descripcion'])

    datos['clima_destino'] = clima_destino
    datos['gif_destino'] = seleccionarGif(clima_destino['descripcion'])

    print(f"GIF origen: {datos['gif_origen']}")
    print(f"GIF destino: {datos['gif_destino']}")

    session['datos'] = datos

    return redirect(url_for('resultado'))

#Manda los datos al Front2.html donde se va a visualizar los elementos obtenidos.
@app.route('/resultado')
def resultado():
    datos = session.get('datos', {})
    return render_template('Front2.html', datos = datos)

if __name__ == '__main__':
    app.run(debug = True)
