#Se importan los elementos que se van a usar, flask, pandas y la api.
from flask import Flask, request, session, render_template, redirect, url_for 
from dotenv import load_dotenv
import pandas as pd
import requests
import os

app = Flask(__name__)
app.secret_key = 'waos'

ubicacion_archivo = os.path.dirname(os.path.abspath(__file__))

csv_camino = os.path.join(ubicacion_archivo, 'static', 'Recursos', 'ubicaciones.csv')

ubicaciones = pd.read_csv(csv_camino)

load_dotenv()
API_KEY = os.getenv('APIK')

if API_KEY is None:
    raise ValueError("La clave API no se ha cargado correctamente.")

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
        }
        cache_clima[clave_cache] = clima
        return clima
    else:
        return None

def obtenerGifyRecomendacion(descripcion):
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
        return ("Recursos/Imagenes/LluviaElectrica.gif", "Busca refugio. Evita estar cerca de elementos metálicos.")
    
    elif ("light intensity drizzle" in descripcion or 
          "light intensity drizzle rain" in descripcion or
          "light rain" in descripcion):
        return ("Recursos/Imagenes/LluviaLL.gif", "Se recomienda llevar paraguas.")
    
    elif ("drizzle" in descripcion or
          "drizzle rain'" in descripcion or
          "heavy intensity drizzle rain" in descripcion or
          "shower rain and drizzle" in descripcion or
          "shower drizzle" in descripcion):
        return ("Recursos/Imagenes/LluviaL.gif", "Se recomienda llevar chamarra y paraguas.")
    
    elif  ("moderate rain" in descripcion or
           "heavy intensity drizzle" in descripcion or
           "heavy shower rain and drizzle" in descripcion):
        return ("Recursos/Imagenes/LluviaM.gif", "Se recomienda llevar paraguas e impermeable.")
    
    elif  ("very heavy rain" in descripcion or
           "heavy intensity rain" in descripcion or
           "extreme rain" in descripcion or
           "light intensity shower rain" in descripcion or
           "shower rain" in descripcion or
           "heavy intensity shower rain" in descripcion or
           "ragged shower rain" in descripcion):
        return ("Recursos/Imagenes/LluviaH.gif", "Se recomienda no salir. A menos que sea necesario, lleva paraguas, impermeable y ten mucha precaución.")
    
    elif ("Sleet" in descripcion or
          "Light shower sleet" in descripcion or
          "Shower sleet" in descripcion or
          "squalls" in descripcion or
          "freezing rain" in descripcion):
        return ("Recursos/Imagenes/AguaNieve.gif", "Se recomienda llevar abrigo y paraguas.")
    
    elif ("light snow" in descripcion or
          "Snow" in descripcion):
        return ("Recursos/Imagenes/NevandoL.gif", "Se recomienda ir abrigado y tener precaución.")
    
    elif ("Heavy snow" in descripcion or
          "Light rain and snow" in descripcion or
          "Rain and snow" in descripcion or
          "Light shower snow" in descripcion or
          "Shower snow" in descripcion or
          "Heavy shower snow" in descripcion):
        return ("Recursos/Imagenes/Nevando.gif", "Se recomienda no salir. En dado caso, ir abrigado y llevar el equipo necesario.")
    
    elif ("tornado" in descripcion):
        return ("Recursos/Imagenes/Tornado.gif", "Ten extrema precaución, no salgas, busca refugio, preferentemente sotanos.")
    
    elif ("clear sky" in descripcion):
        return ("Recursos/Imagenes/Despejado.jpg", "Disfruta, si la temperatura lo permite :).")
    
    elif ("mist" in descripcion or
          "smoke" in descripcion or
          "haze" in descripcion or
          "fog" in descripcion or
          "dust" in descripcion):
        return ("Recursos/Imagenes/Neblina.gif", "Ten extrema precaución. Si es posible no te desplazes.")
    
    elif ("sand" in descripcion or
          "dust whirls" in descripcion):
        return ("Recursos/Imagenes/Arena.gif", "Se recomienda permanecer en interiores. Usa mascarilla y un protector para los ojos si vas a salir." )
    
    elif ("volcanic ash" in descripcion):
        return ("Recursos/Imagenes/Ceniza.gif", "Se recomienda permanecer en interiores. Si vas a salir usa mascarillas y protectores para los ojos." )
    
    elif("few clouds" in descripcion):
        return ("Recursos/Imagenes/NubladoL.jpg", "No se requiere precaución especial.")
    
    elif("scattered clouds" in descripcion):
        return ("Recursos/Imagenes/NubladoLM.gif", "No se requiere precaución especial.")
    
    elif("broken clouds" in descripcion):
        return ("Recursos/Imagenes/NubladoM.jpg", "No se requiere precaución especial.")
    
    elif("overcast clouds" in descripcion):
        return ("Recursos/Imagenes/NubladoH.gif", "No se requiere precaución especial.")
    
    else: 
        return ("Recursos/Imagenes/Default.gif", "...")

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

def obtenerRecomendacionTemp(temperatura):
    if temperatura < 1:
        return "Hace demasiado frío, ve lo más abrigado posible y usa ropa térmica."
    elif 1 <= temperatura <= 10:
        return "Hace bastante frío, usa chamarra."
    elif 10 <= temperatura <= 16:
        return "Es un clima fresco, lleva una chaqueta."
    elif 16 <= temperatura <= 22:
        return "Es un clima agradable, usa ropa ligera."
    elif 22 <= temperatura <= 29:
        return "Es un clima calido, ve con ropa fresca."
    elif temperatura >= 30:
        return "Hace demasiado calor, usa ropa fresca y mantente hidratado."
    else:
        return "No se requiere precaución especial."
     
#Se declara la ruta de inicio.
@app.route('/')
def index():
    return render_template('Front.html')

#Se declará los elementos que se van a procesar, en este caso buscar en el csv los parametros otorgados en el front.html
@app.route('/procesar', methods=['POST'])
def procesar():
    session.clear()
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
    gifOrigen, nada = obtenerGifyRecomendacion(clima_origen['descripcion'])
    datos['gif_origen'] = gifOrigen
    #datos['gif_origen'] = seleccionarGif(clima_origen['descripcion'])
    datos['clima_origen']['descripcion_traducida'] = traducirDescripcion(clima_origen['descripcion'])


    datos['clima_destino'] = clima_destino
    gifDestino, recomendacion = obtenerGifyRecomendacion(clima_destino['descripcion'])
    datos['gif_destino'] = gifDestino
    datos['recomendacion_destino'] = recomendacion
    datos['clima_destino']['descripcion_traducida'] = traducirDescripcion(clima_destino['descripcion'])
    datos['recomendacion_temp_destino'] = obtenerRecomendacionTemp(clima_destino['temperatura'])

    session['datos'] = datos
    return redirect(url_for('resultado'))

#Manda los datos al Front2.html donde se va a visualizar los elementos obtenidos.
@app.route('/resultado')
def resultado():
    datos = session.get('datos', {})
    return render_template('Front2.html', datos = datos)

if __name__ == '__main__':
    app.run(debug = True)
