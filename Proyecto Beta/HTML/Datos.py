#Se importan los elementos que se van a usar, flask, pandas y la api.
from flask import Flask, request, render_template, redirect, url_for, session
import pandas as pd
import requests
import os

app = Flask(__name__)
app.secret_key = 'waos'

#Vincular Base de datos con este programa:
#Se le pide por favor que ingrese su dirección de archivo local para que funcione esté elemento.
ubicaciones = pd.read_csv('E:/Cardinal/Github/Primer-Proyecto-MYP/Proyecto Beta/HTML/static/Recursos/ubicaciones.csv')

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
    print(f"Descripción otorgada: {descripcion}")
    if ("thunderstorm with light rain" in descripcion or 
        "thunderstorm with rain" in descripcion or 
        "thunderstorm with heavy rain" in descripcion or 
        "light thunderstorm" in descripcion or 
        "thunderstorm" in descripcion or 
        "heavy thunderstorm" in descripcion or 
        "ragged thunderstorm" in descripcion or 
        "thunderstorm with light drizzle" in descripcion or 
        "thunderstorm with drizzle" in descripcion or 
        "thunderstorm with heavy drizzle" in descripcion):
        return "Recursos/Imagenes/LluviaElectrica.gif"
    
    elif ("light intensity drizzle" in descripcion or 
          "light intensity drizzle rain" in descripcion or
          "light rain" in descripcion):
        return "Recursos/Imagenes/LluviaLL.gif"
    
    elif ("drizzle" in descripcion or
          "drizzle rain'" in descripcion or
          "heavy intensity drizzle rain" in descripcion or
          "shower rain and drizzle" in descripcion or
          "shower drizzle" in descripcion):
        return "Recursos/Imagenes/LluviaL.gif"
    
    elif  ("moderate rain" in descripcion or
           "heavy intensity drizzle" in descripcion or
           "heavy shower rain and drizzle" in descripcion):
        return "Recursos/Imagenes/LluviaM.gif"
    
    elif  ("very heavy rain" in descripcion or
           "heavy intensity rain" in descripcion or
           "extreme rain" in descripcion or
           "light intensity shower rain" in descripcion or
           "shower rain" in descripcion or
           "heavy intensity shower rain" in descripcion or
           "ragged shower rain" in descripcion):
        return "Recursos/Imagenes/LluviaH.gif"
    
    elif ("Sleet" in descripcion or
          "Light shower sleet" in descripcion or
          "Shower sleet" in descripcion or
          "squalls" in descripcion or
          "freezing rain" in descripcion):
        return "Recursos/Imagenes/AguaNieve.gif"
    
    elif ("light snow" in descripcion or
          "Snow" in descripcion):
        return "Recursos/Imagenes/NevandoL.gif"
    
    elif ("Heavy snow" in descripcion or
          "Light rain and snow" in descripcion or
          "Rain and snow" in descripcion or
          "Light shower snow" in descripcion or
          "Shower snow" in descripcion or
          "Heavy shower snow" in descripcion):
        return "Recursos/Imagenes/Nevando.gif"
    
    elif ("tornado" in descripcion):
        return "Recursos/Imagenes/Tornado.gif"
    
    elif ("clear sky" in descripcion):
        return "Recursos/Imagenes/Despejado.jpg"
    
    elif ("mist" in descripcion or
          "smoke" in descripcion or
          "haze" in descripcion or
          "fog" in descripcion or
          "dust" in descripcion):
        return "Recursos/Imagenes/Neblina.gif"
    
    elif ("sand" in descripcion or
          "dust whirls" in descripcion):
        return "Recursos/Imagenes/Arena.gif"
    
    elif ("volcanic ash" in descripcion):
        return "Recursos/Imagenes/Ceniza.gif"
    
    elif("few clouds" in descripcion):
        return "Recursos/Imagenes/NubladoL.jpg"
    
    elif("scattered clouds" in descripcion):
        return "Recursos/Imagenes/NubladoLM.gif"
    
    elif("broken clouds" in descripcion):
        return "Recursos/Imagenes/NubladoM.jpg"
    
    elif("overcast clouds" in descripcion):
        return "Recursos/Imagenes/NubladoH.gif"
    
    else: 
        return "Recursos/Imagenes/Default.gif"

traducciones = {
    "thunderstorm with light rain": "Tormenta con lluvia ligera.",
    "thunderstorm with rain": "Tormenta con lluvia.",
    "thunderstorm with heavy rain": "Tormenta con lluvia fuerte.",
    "light thunderstorm": "Tormenta ligera.",
    "thunderstorm": "Tormenta.",
    "heavy thunderstorm": "Tormenta fuerte.",
    "ragged thunderstorm": "Tormenta irregular.",
    "thunderstorm with light drizzle": "Tormenta con llovizna ligera.",
    "thunderstorm with drizzle": "Tormenta con llovizna.",
    "thunderstorm with heavy drizzle": "Tormenta con llovizna fuerte.",
    "light intensity drizzle": "Llovizna de intensidad ligera.",
    "light intensity drizzle rain": "Lluvia de llovizna ligera.",
    "light rain": "Lluvia ligera.",
    "drizzle": "Llovizna.",
    "drizzle rain": "Lluvia de llovizna.",
    "heavy intensity drizzle rain": "Lluvia de llovizna intensa.",
    "shower rain and drizzle": "Chubasco y llovizna.",
    "shower drizzle": "Chubasco de llovizna.",
    "moderate rain": "Lluvia moderada.",
    "heavy intensity drizzle": "Llovizna intensa.",
    "heavy shower rain and drizzle": "Chubasco fuerte y llovizna.",
    "very heavy rain": "Lluvia muy fuerte.",
    "heavy intensity rain": "Lluvia de intensidad fuerte.",
    "extreme rain": "Lluvia extrema.",
    "light intensity shower rain": "Chubasco de intensidad ligera.",
    "shower rain": "Chubasco.",
    "heavy intensity shower rain": "Chubasco de intensidad fuerte.",
    "ragged shower rain": "Chubasco irregular.",
    "sleet": "Aguanieve.",
    "light shower sleet": "Chubasco ligero de aguanieve.",
    "shower sleet": "Chubasco de aguanieve.",
    "squalls": "Ráfagas.",
    "freezing rain": "Lluvia helada.",
    "light snow": "Nieve ligera.",
    "snow": "Nieve.",
    "heavy snow": "Nieve fuerte.",
    "light rain and snow": "Lluvia ligera y nieve.",
    "rain and snow": "Lluvia y nieve.",
    "light shower snow": "Chubasco ligero de nieve.",
    "shower snow": "Chubasco de nieve.",
    "heavy shower snow": "Chubasco fuerte de nieve.",
    "tornado": "Tornado.",
    "clear sky": "Cielo despejado.",
    "mist": "Niebla.",
    "smoke": "Humo.",
    "haze": "Bruma.",
    "fog": "Niebla.",
    "dust": "Polvo.",
    "sand": "Arena.",
    "dust whirls": "Remolinos de polvo.",
    "volcanic ash": "Ceniza volcánica.",
    "few clouds": "Pocas nubes.",
    "scattered clouds": "Nubes dispersas.",
    "broken clouds": "Nubes fragmentadas.",
    "overcast clouds": "Nubes cubiertas."
}

def traducirDescripcion(descripcion):
    for en, es in traducciones.items():
        descripcion = descripcion.replace(en, es)
    return descripcion

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
    clima_origen['descripcion'] = traducirDescripcion(clima_origen['descripcion'])


    datos['clima_destino'] = clima_destino
    datos['gif_destino'] = seleccionarGif(clima_destino['descripcion'])
    clima_destino['descripcion'] = traducirDescripcion(clima_destino['descripcion'])

    session['datos'] = datos
    return redirect(url_for('resultado'))

#Manda los datos al Front2.html donde se va a visualizar los elementos obtenidos.
@app.route('/resultado')
def resultado():
    datos = session.get('datos', {})
    return render_template('Front2.html', datos = datos)

if __name__ == '__main__':
    app.run(debug = True)
