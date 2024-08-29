from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/procesar', methods=['POST'])
def procesar():
    data = request.get_json()
    parametro1 = data.get('Parametro1')
    parametro2 = data.get('Parametro2')

    # Apartado en el que va la API. Código de testeo.
    if parametro1 == parametro2:
        return jsonify(success = False, message="Las opciones no pueden ser iguales")
    else:
        #Procesa los datos y guarda en un archivo, base de datos, etc.
        return jsonify(success=True, message="Datos procesador", parametro1=parametro1, parametro2=parametro2)
@app.route('/resultado')
def resultado():
    parametro1 = request.args.get('parametro1')
    parametro2 = request.args.get('parametro2')
    return render_template('Front2.html', parametro1 = parametro1, parametro2 = parametro2)    
if __name__ == '__main__':
    app.run(debug=True)