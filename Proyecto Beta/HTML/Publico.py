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
    '''
    Esta función otorga los datos para que la api regrese la información solicitada.

    Parametros: 
    latitud(int): La latitud de la ubicacion.
    longitud(int): La longitud de la ubicación.

    Retorna:
    dict: Datos del clima o None en caso de error.

    '''
    clave_cache = f"{latitud},{longitud}"
    if clave_cache in cache_clima:
        return cache_clima[clave_cache]
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitud}&lon={longitud}&appid={API_KEY}&units=metric"
    try:
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            datos_clima = respuesta.json()
            if isinstance(datos_clima, dict) and 'main' in datos_clima and 'weather' in datos_clima:
                clima = {
                    'temperatura': datos_clima['main']['temp'],
                    'sensacion_termica': datos_clima['main']['feels_like'],
                    'descripcion': datos_clima['weather'][0]['description'],
                }
                cache_clima[clave_cache] = clima
                return clima
            else:
                error_message = "Formato de respuesta no válido."
        elif respuesta.status_code == 404:
            error_message = "La ubicación no se encuentra en la API."
        elif respuesta.status_code == 401:
            error_message = "Error de autenticación. Verifica tu clave de API."
        else:
            error_message = f"Error inesperado: {respuesta.status_code}"
    except requests.exceptions.ConnectionError:
        error_message = "Error de conexión. Verifica tu conexión a Internet."
    except requests.exceptions.Timeout:
        error_message = "Error de tiempo de espera. La solicitud tardó demasiado en responder."
    except requests.exceptions.RequestException as e:
        error_message = f"Se produjo un error en la solicitud: {e}"
    except TypeError as e:
        error_message = f"Error de tipo: {e}"
    
    return redirect(url_for('error_page', error_message=error_message))

def obtenerGifyRecomendacion(descripcion, esPrimerDescripcion):
    '''
    Función que dependiendo lo recibido, seleccione un gif y una descripción.

    Parametros:
    descripcion(String): La descripcion dada.
    esPrimerDescripcion(boolean): Verifica si es la primer descripción.

    Return
    gif: El gif obtenido a base de la descripción.
    String: Recomendación.
    '''
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
        if esPrimerDescripcion:
            return ("Recursos/Imagenes/LluviaElectrica.gif", "Debido al mal clima, puede que tu vuelo se demore.")
        else:
            return ("Recursos/Imagenes/LluviaElectrica.gif", "Busca refugio. Evita estar cerca de elementos metálicos.")
    
    elif ("light intensity drizzle" in descripcion or 
          "light intensity drizzle rain" in descripcion or
          "light rain" in descripcion):
        if esPrimerDescripcion:
            return ("Recursos/Imagenes/LluviaLL.gif", "Tu vuelo debe salir a tiempo.")
        else:
            return ("Recursos/Imagenes/LluviaLL.gif", "Se recomienda llevar paraguas.")
    
    elif ("drizzle" in descripcion or
          "drizzle rain'" in descripcion or
          "heavy intensity drizzle rain" in descripcion or
          "shower rain and drizzle" in descripcion or
          "shower drizzle" in descripcion):
        if esPrimerDescripcion:
            return(("Recursos/Imagenes/LluviaL.gif", "Tu vuelo debe salir a tiempo."))
        else:
            return ("Recursos/Imagenes/LluviaL.gif", "Se recomienda llevar chamarra y paraguas.")
    
    elif  ("moderate rain" in descripcion or
           "heavy intensity drizzle" in descripcion or
           "heavy shower rain and drizzle" in descripcion):
        if esPrimerDescripcion:
            return ("Recursos/Imagenes/LluviaM.gif", "Tu vuelo puede demorarse un poco.")
        else:
            return ("Recursos/Imagenes/LluviaM.gif", "Se recomienda llevar paraguas e impermeable.")
    
    elif  ("very heavy rain" in descripcion or
           "heavy intensity rain" in descripcion or
           "extreme rain" in descripcion or
           "light intensity shower rain" in descripcion or
           "shower rain" in descripcion or
           "heavy intensity shower rain" in descripcion or
           "ragged shower rain" in descripcion):
        if esPrimerDescripcion:
            return (("Recursos/Imagenes/LluviaH.gif", "Tu vuelo se va a demorar o cancelar."))
        else:
            return ("Recursos/Imagenes/LluviaH.gif", "Se recomienda no salir. A menos que sea necesario, lleva paraguas, impermeable y ten mucha precaución.")
    
    elif ("Sleet" in descripcion or
          "Light shower sleet" in descripcion or
          "Shower sleet" in descripcion or
          "squalls" in descripcion or
          "freezing rain" in descripcion):
        if esPrimerDescripcion:
            return ("Recursos/Imagenes/AguaNieve.gif", "Tu vuelo debe salir a tiempo.")
        else:
            return ("Recursos/Imagenes/AguaNieve.gif", "Se recomienda llevar abrigo y paraguas.")
    
    elif ("light snow" in descripcion or
          "Snow" in descripcion):
        if esPrimerDescripcion:
            return ("Recursos/Imagenes/NevandoL.gif", "Tu vuelo debe salir a tiempo.")
        else:
            return ("Recursos/Imagenes/NevandoL.gif", "Se recomienda ir abrigado y tener precaución.")
    
    elif ("Heavy snow" in descripcion or
          "Light rain and snow" in descripcion or
          "Rain and snow" in descripcion or
          "Light shower snow" in descripcion or
          "Shower snow" in descripcion or
          "Heavy shower snow" in descripcion):
        if esPrimerDescripcion:
            return (("Recursos/Imagenes/Nevando.gif", "Tu vuelo se va a demorar o reprogramar."))
        else:
            return ("Recursos/Imagenes/Nevando.gif", "Se recomienda no salir. En dado caso, ir abrigado y llevar el equipo necesario.")
    
    elif ("tornado" in descripcion):
        if esPrimerDescripcion:
            return (("Recursos/Imagenes/Tornado.gif", "Tu vuelo se va a cancelar, se debe de reprogramar."))
        else:
            return ("Recursos/Imagenes/Tornado.gif", "Ten extrema precaución, no salgas, busca refugio, preferentemente sotanos.")
    
    elif ("clear sky" in descripcion):
        if esPrimerDescripcion:
            return ("Recursos/Imagenes/Despejado.jpg", "Tu vuelo debe salir a tiempo.")
        else:
            return ("Recursos/Imagenes/Despejado.jpg", "Disfruta, si la temperatura lo permite :).")
    
    elif ("mist" in descripcion or
          "smoke" in descripcion or
          "haze" in descripcion or
          "fog" in descripcion or
          "dust" in descripcion):
        if esPrimerDescripcion:
            return (("Recursos/Imagenes/Neblina.gif", "Tu vuelo se puede demorar."))
        else:
            return ("Recursos/Imagenes/Neblina.gif", "Ten extrema precaución. Si es posible no te desplazes.")
    
    elif ("sand" in descripcion or
          "dust whirls" in descripcion):
        if esPrimerDescripcion:
            return (("Recursos/Imagenes/Arena.gif", "Tu vuelo se va a demorar."))
        else:
            return ("Recursos/Imagenes/Arena.gif", "Se recomienda permanecer en interiores. Usa mascarilla y un protector para los ojos si vas a salir." )
    
    elif ("volcanic ash" in descripcion):
        if esPrimerDescripcion:
            return ("Recursos/Imagenes/Ceniza.gif", "Tu vuelo se va a demorar, reprogramarse o incluso cancelarse.")
        else:
            return ("Recursos/Imagenes/Ceniza.gif", "Se recomienda permanecer en interiores. Si vas a salir usa mascarillas y protectores para los ojos." )
    
    elif("few clouds" in descripcion):
        if esPrimerDescripcion:
            return ("Recursos/Imagenes/NubladoL.jpg", "Tu vuelo debe salir a tiempo.")
        else:
            return ("Recursos/Imagenes/NubladoL.jpg", "No se requiere precaución especial.")
    
    elif("scattered clouds" in descripcion):
        if esPrimerDescripcion:
            return ("Recursos/Imagenes/NubladoLM.gif", "Tu vuelo debe salir a tiempo.")
        else:
            return ("Recursos/Imagenes/NubladoLM.gif", "No se requiere precaución especial.")
    
    elif("broken clouds" in descripcion):
        if esPrimerDescripcion:
            return ("Recursos/Imagenes/NubladoM.jpg", "Tu vuelo debe salir a tiempo.")
        else:
            return ("Recursos/Imagenes/NubladoM.jpg", "No se requiere precaución especial.")
    
    elif("overcast clouds" in descripcion):
        if esPrimerDescripcion:
            return ("Recursos/Imagenes/NubladoH.gif", "Tu vuelo debe salir a tiempo.")
        else:
            return ("Recursos/Imagenes/NubladoH.gif", "No se requiere precaución especial.")
    
    else: 
        return ("Recursos/Imagenes/Default.gif", "...")
    
def asignarGifyRecomendacion(descripcion1, descripcion2):
    '''
    Función que maneja dos descripciones y da el gif y la recomendación de dichas descripciones.

    Parametros:
    descripcion1(String): La primera descripción dada.
    descripcion2(String): La segunda descripción dada.

    Return
    gif1: El gif obtenido de la primer descripción.
    estado: El estado obtenido de la primer descripción.
    gif2: El gif obtenido de la segunda descripción.
    recomendación: La recomendación de la segunda descripción.
    '''
    gif1, estado = obtenerGifyRecomendacion(descripcion1, True)
    gif2, recomendacion = obtenerGifyRecomendacion(descripcion2, False)

    return gif1, estado, gif2, recomendacion

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
    '''
    Función que traduce lo recibido.

    Argumentos:
    descripcion (String): El texto a traducir.

    Retorno:
    String: Texto traducido.
    '''
    for en, es in traducciones.items():
        descripcion = descripcion.replace(en, es)
    return descripcion

def obtenerRecomendacionTemp(temperatura):
    '''
    Función que da una recomendación basada en los datos recibidos.

    Argumentos:
    temperatura (int): Los datos que da la api respecto a dicho parametro.

    Retorno:
    (String): Recomendación dada a base de la temperatura.
    '''
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
     
@app.route('/')
def index():
    '''
    Definición que inicializa la ruta de inicio.

    Retorno:
    La ruta de inicio.
    '''
    return render_template('Front.html')

#Se declará los elementos que se van a procesar, en este caso buscar en el csv los parametros otorgados en el front.html
@app.route('/procesar', methods=['POST'])
def procesar():
    '''
    Definición que procesa todos los datos solicitados en el archivo de trabajo.

    Retorno:
    Los datos procesados

    '''
    session.clear()
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
            'origenLatitud': filtroOrigen.iloc[0]['origin_latitude'] if not filtroOrigen.empty else "No disponible",
            'origenLongitud': filtroOrigen.iloc[0]['origin_longitude'] if not filtroOrigen.empty else "No disponible",
            'destinoLatitud': filtroDestino.iloc[0]['destination_latitude'] if not filtroDestino.empty else "No disponible",
            'destinoLongitud': filtroDestino.iloc[0]['destination_longitude'] if not filtroDestino.empty else "No disponible",
            'origen': origen,
            'destino': destino
        }
    clima_origen = obtener_clima(datos['origenLatitud'], datos['origenLongitud'])
    clima_destino = obtener_clima(datos['destinoLatitud'], datos['destinoLongitud'])

    gifOrigen, estado, gifDestino, recomendacion = asignarGifyRecomendacion(clima_origen['descripcion'], clima_destino['descripcion'])
    datos['clima_origen'] = clima_origen
    datos['estado_origen'] = estado
    datos['gif_origen'] = gifOrigen
    datos['clima_origen']['descripcion_traducida'] = traducirDescripcion(clima_origen['descripcion'])


    datos['clima_destino'] = clima_destino
    datos['gif_destino'] = gifDestino
    datos['recomendacion_destino'] = recomendacion
    datos['clima_destino']['descripcion_traducida'] = traducirDescripcion(clima_destino['descripcion'])
    datos['recomendacion_temp_destino'] = obtenerRecomendacionTemp(clima_destino['temperatura'])

    session['datos'] = datos
    return redirect(url_for('resultado'))

@app.route('/resultado')
def resultado():
    '''
    Funcion que presenta los datos procesados.

    Retorno:
    El lugar en el que se presentan los datos ya procesados.
    '''
    datos = session.get('datos', {})
    return render_template('Front2.html', datos = datos)

@app.route('/error')
def error_page():
    error_message = request.args.get('error_message', 'Unknown error')
    return render_template('error.html', error_message=error_message)

@app.route('/prueba_error')
def prueba_error():
    return redirect(url_for('error_page', error_message="Este es un error de prueba."))

if __name__ == '__main__':
    app.run(debug = True)
