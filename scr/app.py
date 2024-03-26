from flask import Flask, request, jsonify
from flask_cors import CORS

import pandas as pd
import numpy as np
import datetime
from datetime import datetime, timedelta


from statsmodels.tsa.arima.model import ARIMA

### para segmentacion
import json
### fin import segmentacion


#===============================================================================================================================
#
#       ESTE ES EL CUERPO DE LA APP DE VENTAS
#
#===============================================================================================================================


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["https://develop--despliegueprueba.netlify.app", "https://otrodominio.com"]}})  # Agrega múltiples dominios a la lista blanca de CORS

#===============================================================================================================================
# Endpoint HOME 
#==============================================================================================================================

@app.route('/', methods=['GET'])
def home():
    return "<h1>Prueba Desafío PREDICCION DE VENTAS</h1>"



# ==============================================================================================================================
# PREDICCION   --> ( Los datos los pasamos por la URL ) [GET] )
# ==============================================================================================================================

"""
La petición sería tipo:
http://127.0.0.1:5000/api/v1/ventas/predict?ubicacion=the_bridge&maquina=vitrina&producto=agua&fecha=2024-03-21    
"""

@app.route('/api/v1/ventas/predict', methods = ['GET']) 
#['GET']: Aquí cogemos los argumentos por ubicacion, maquina, producto y fecha por URL con 'request.arg'
def predict():
    args = request.args
    if 'ubicacion' in args and 'maquina' in args and 'producto' in args and 'fecha' in args:
        
        # Recuperamos los parametros 
        ubicacion = args.get('ubicacion', None)
        maquina = args.get('maquina', None)
        Producto = args.get('producto', None)
        fecha_query = args.get('fecha', None) 

        # Comprobamos los parametros
        if ubicacion is None or maquina is None or Producto is None or fecha_query is None:
            return "Error. Args empty"
        else:

            # Transformamos y declaramos variables
            fecha_prediccion = datetime.strptime(fecha_query, '%Y-%m-%d') + timedelta(days=7)
            fecha_prediccion = fecha_prediccion.strftime('%Y-%m-%d')       
            Frecuencia = "h"
            ubicacion = str.lower(ubicacion)
            maquina = str.lower(maquina)
            Producto = str.lower(Producto)

            # Cargamos la BBDD
            # df = pd.read_csv('/home/ubuntu/prod/endpoint/bbdd_consolidado.csv')
            df = pd.read_csv("./bbdd_consolidado.csv")
            df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S')

            # Creamos el filtro a la BBDD por producto y fecha y la muestra, que es el X
            Consolidado = df.loc[df["Product"]== Producto] 
            muestra = Consolidado.groupby(pd.Grouper(key="Date", freq=Frecuencia)).count().sort_index().drop(["Product"],axis=1)

            # Entrenamos el modelo 
            ARIMAmodel = ARIMA(muestra, order = (2,0,2),seasonal_order=(2,1,0,12))
            model = ARIMAmodel.fit()
            prediccion = model.predict(start=fecha_query, end=fecha_prediccion)

            # Con la prediccion, la procesamos y...
            prediccion_df = pd.DataFrame(prediccion)
            prediccion_df.rename(columns={'predicted_mean': 'prediccion'}, inplace=True)
            prediccion_df['prediccion'] = np.round(prediccion_df['prediccion'])
            prediccion_df.reset_index(inplace=True)
            prediccion_df.rename(columns={'index': 'fecha'}, inplace=True)
            prediccion_df['prediccion'] = prediccion_df['prediccion'].astype('int')
            prediccion_df = prediccion_df.groupby(pd.Grouper(key="fecha", freq='d')).sum()

            # ...generamos el JSON de respuesta
            respuesta = [
                {'ubicacion' : ubicacion},
                {'maquina' : maquina},
                {'producto' : Producto},
            ]
            for row in prediccion_df.iterrows():
                respuesta.append({str(row[0].strftime('%Y-%m-%d')) : str(row[1]['prediccion'])})  

            return jsonify(respuesta)     
            
    else:
        return "Error in args"


### codigo segmentacion
@app.route('/api/v1/segmentacion/', methods=['GET'])
def paso_jayson():
        with open('./json_vending_schiller_DEF.json', 'r') as prod:
            file = json.load(prod)
            return jsonify(file)


### fin codigo segmentacion




if __name__ == "__main__":
    app.run(debug=False)
