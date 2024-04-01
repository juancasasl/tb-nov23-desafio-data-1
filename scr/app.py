from flask import Flask, request, jsonify
from flask_cors import CORS

import pandas as pd
import numpy as np
import datetime as dt
from datetime import datetime, timedelta


### para segmentacion
import json
### fin import segmentacion


#===============================================================================================================================
#
#       ESTE ES EL CUERPO DE LA APP DE VENTAS
#
#===============================================================================================================================


app = Flask(__name__)
CORS(app)
#CORS(app, resources={r"/api/*": {"origins": ["https://develop--despliegueprueba.netlify.app", "https://despliegueprueba.netlify.app/", "https://otrodominio.com"]}})  # Agrega múltiples dominios a la lista blanca de CORS

#===============================================================================================================================
# Endpoint HOME 
#==============================================================================================================================

@app.route('/', methods=['GET'])
def home():
    return "<h1>Prueba Desafío TOTAL</h1>"



### codigo prediccion

# ==============================================================================================================================
# ENDPOINT 3 - ANALITICA GENERAL   --> ( Los datos los pasamos por la URL ) [GET] )
# ==============================================================================================================================

"""
La petición sería tipo:

http://127.0.0.1:5000/api/v1/ventas/general/analitica-general?ubicacion=the-bridge
o
http://127.0.0.1:5000/api/v1/ventas/general/analitica-general?ubicacion=schiller

"""

@app.route('/api/v1/ventas/general/analitica-general', methods = ['GET']) 
#['GET']: Aquí cogemos los argumentos por producto y fecha por URL con 'request.arg'
def analitica_general():

    args = request.args
    if 'ubicacion' in args:

        ubi = args.get('ubicacion', None)

        if ubi not in list(df['ubicacion'].unique()):
            return "Error. Incorrect arguments"
        else:

            if ubi == 'the-bridge':
                fecha = '2024-03-12'
                df_ventas = df_tb
                df_predict = df_pred_tb
            elif ubi == 'schiller':
                fecha = '2024-03-21'
                df_ventas = df_sc
                df_predict = df_pred_sc

            fecha_sep = pd.to_datetime(fecha)
            fecha_start = fecha_sep - timedelta(6)  # 2024-03-06 (TB) o 2024-03-15 (SCHILLER)
            fecha_fin = fecha_sep + timedelta(7)    # 2024-03-19 (TB) o 2024-03-28 (SCHILLER)

            df_ventas = df_ventas[(df_ventas['fecha'] >= fecha_start) & (df_ventas['fecha'] <= fecha_sep + timedelta(1))]
            df_ventas = df_ventas.groupby(pd.Grouper(key='fecha', freq='d')).count()
            df_ventas.reset_index(inplace=True)                

            df_predict = df_predict[(df_predict['fecha'] > fecha_sep) & (df_predict['fecha'] <= fecha_fin)]
            df_predict = df_predict.groupby(pd.Grouper(key='fecha', freq='d')).sum()
            df_predict.reset_index(inplace=True)

            objeto_ventas = {}
            for index, row in df_ventas.iterrows():
                if row['fecha'].weekday() != 6:
                    objeto_ventas[row['fecha'].strftime('%Y-%m-%d')] = str(row['producto'])
            
            objeto_predicciones = {}
            for index, row in df_predict.iterrows():
                if row['fecha'].weekday() != 6:
                    objeto_predicciones[row['fecha'].strftime('%Y-%m-%d')] = str(row['prediccion'])
                    
            respuesta = [{'ubicacion':ubi}, objeto_ventas, objeto_predicciones]

            return jsonify(respuesta)
        
    else:
        return "Error in args"
   




# ==============================================================================================================================
# ENDPOINT 4 - ANALITICA / MAQUINA   --> ( Los datos los pasamos por la URL ) [GET] )
# ==============================================================================================================================

"""
La petición sería tipo:

http://127.0.0.1:5000/api/v1/ventas/analitica/maquina?ubicacion=the-bridge&maquina=cafe
o
http://127.0.0.1:5000/api/v1/ventas/analitica/maquina?ubicacion=schiller&maquina=snack

"""

@app.route('/api/v1/ventas/analitica/maquina', methods = ['GET']) 
#['GET']: Aquí cogemos los argumentos por producto y fecha por URL con 'request.arg'
def analitica_por_maquina():

    args = request.args
    if ('ubicacion' in args) and ('maquina' in args):

        ubi = args.get('ubicacion', None)
        maq = args.get('maquina', None)

        if (ubi not in list(df['ubicacion'].unique()))\
            and (maq not in list(df['maquina'].unique())):
            return "Error. Incorrect arguments"
        else:

            if ubi == 'the-bridge':
                fecha = '2024-03-12'
                df_ventas = df_tb
                df_predict = df_pred_tb
            elif ubi == 'schiller':
                fecha = '2024-03-21'
                df_ventas = df_sc
                df_predict = df_pred_sc

            fecha_sep = pd.to_datetime(fecha)
            fecha_start = fecha_sep - timedelta(6)  # 2024-03-06 (TB) o 2024-03-15 (SCHILLER)
            fecha_fin = fecha_sep + timedelta(7)    # 2024-03-19 (TB) o 2024-03-28 (SCHILLER)
            
            df_ventas = df_ventas[df_ventas['maquina'] == maq]
            df_ventas = df_ventas[(df_ventas['fecha'] >= fecha_start) & (df_ventas['fecha'] <= fecha_sep + timedelta(1))]
            df_ventas = df_ventas.groupby(pd.Grouper(key='fecha', freq='d')).count()
            df_ventas.reset_index(inplace=True)

            df_predict = df_predict[df_predict['maquina'] == maq]
            df_predict = df_predict[(df_predict['fecha'] > fecha_sep) & (df_predict['fecha'] <= fecha_fin)]
            df_predict = df_predict.groupby(pd.Grouper(key='fecha', freq='d')).sum()
            df_predict.reset_index(inplace=True)

            objeto_ventas = {}
            for index, row in df_ventas.iterrows():
                if row['fecha'].weekday() != 6:
                    objeto_ventas[row['fecha'].strftime('%Y-%m-%d')] = str(row['producto'])
            
            objeto_predicciones = {}
            for index, row in df_predict.iterrows():
                if row['fecha'].weekday() != 6:
                    objeto_predicciones[row['fecha'].strftime('%Y-%m-%d')] = str(row['prediccion'])
                    
            respuesta = [{'ubicacion':ubi, 'maquina':maq}, objeto_ventas, objeto_predicciones]

            return jsonify(respuesta)
        
    else:
        return "Error in args"
   




# ==============================================================================================================================
# ENDPOINT 5 - ANALITICA / MAQUINA / CATEGORIA   --> ( Los datos los pasamos por la URL ) [GET] )
# ==============================================================================================================================

"""
La petición sería tipo:

http://127.0.0.1:5000/api/v1/ventas/analitica/categoria?ubicacion=the-bridge&maquina=cafe&categoria=descafeinado
o
http://127.0.0.1:5000/api/v1/ventas/analitica/categoria?ubicacion=schiller&maquina=snack&categoria=galletas

"""

@app.route('/api/v1/ventas/analitica/categoria', methods = ['GET']) 
#['GET']: Aquí cogemos los argumentos por producto y fecha por URL con 'request.arg'
def analitica_por_categoria():

    args = request.args
    if ('ubicacion' in args) and ('maquina' in args) and ('categoria' in args):

        ubi = args.get('ubicacion', None)
        maq = args.get('maquina', None)
        cat = args.get('categoria', None)

        if (ubi not in list(df['ubicacion'].unique()))\
            and (maq not in list(df['maquina'].unique()))\
            and (cat not in list(df['categoria'].unique())):
            return "Error. Incorrect arguments"
        else:

            if ubi == 'the-bridge':
                fecha = '2024-03-12'
                df_ventas = df_tb
                df_predict = df_pred_tb
            elif ubi == 'schiller':
                fecha = '2024-03-21'
                df_ventas = df_sc
                df_predict = df_pred_sc

            fecha_sep = pd.to_datetime(fecha)
            fecha_start = fecha_sep - timedelta(6)  # 2024-03-06 (TB) o 2024-03-15 (SCHILLER)
            fecha_fin = fecha_sep + timedelta(7)    # 2024-03-19 (TB) o 2024-03-28 (SCHILLER)
            
            df_ventas = df_ventas[(df_ventas['maquina'] == maq) & (df_ventas['categoria'] == cat)]
            df_ventas = df_ventas[(df_ventas['fecha'] >= fecha_start) & (df_ventas['fecha'] <= fecha_sep + timedelta(1))]
            df_ventas = df_ventas.groupby(pd.Grouper(key='fecha', freq='d')).count()
            df_ventas.reset_index(inplace=True)

            df_predict = df_predict[(df_predict['maquina'] == maq) & (df_predict['categoria'] == cat)]
            df_predict = df_predict[(df_predict['fecha'] > fecha_sep) & (df_predict['fecha'] <= fecha_fin)]
            df_predict = df_predict.groupby(pd.Grouper(key='fecha', freq='d')).sum()
            df_predict.reset_index(inplace=True)

            objeto_ventas = {}
            for index, row in df_ventas.iterrows():
                if row['fecha'].weekday() != 6:
                    objeto_ventas[row['fecha'].strftime('%Y-%m-%d')] = str(row['producto'])
            
            objeto_predicciones = {}
            for index, row in df_predict.iterrows():
                if row['fecha'].weekday() != 6:
                    objeto_predicciones[row['fecha'].strftime('%Y-%m-%d')] = str(row['prediccion'])
                    
            respuesta = [{'ubicacion':ubi, 'maquina':maq, 'categoria':cat}, objeto_ventas, objeto_predicciones]

            return jsonify(respuesta)
        
    else:
        return "Error in args"
    




# ==============================================================================================================================
# ENDPOINT 6 - ANALITICA / MAQUINA / CATEGORIA / PRODUCTO  --> ( Los datos los pasamos por la URL ) [GET] )
# ==============================================================================================================================

"""
La petición sería tipo:

http://127.0.0.1:5000/api/v1/ventas/analitica/producto?ubicacion=the-bridge&maquina=cafe&categoria=descafeinado&producto=descafeinado-americano
o
http://127.0.0.1:5000/api/v1/ventas/analitica/producto?ubicacion=schiller&maquina=snack&categoria=galletas&producto=chips-ahoy

"""

@app.route('/api/v1/ventas/analitica/producto', methods = ['GET']) 
#['GET']: Aquí cogemos los argumentos por producto y fecha por URL con 'request.arg'
def analitica_por_producto():

    args = request.args
    if ('ubicacion' in args) and ('maquina' in args) and ('categoria' in args) and ('producto' in args):

        ubi = args.get('ubicacion', None)
        maq = args.get('maquina', None)
        cat = args.get('categoria', None)
        prod = args.get('producto', None)

        if (ubi not in list(df['ubicacion'].unique()))\
            and (maq not in list(df['maquina'].unique()))\
            and (cat not in list(df['categoria'].unique()))\
            and (prod not in list(df['producto'].unique())):
            return "Error. Incorrect arguments"
        else:

            if ubi == 'the-bridge':
                fecha = '2024-03-12'
                df_ventas = df_tb
                df_predict = df_pred_tb
            elif ubi == 'schiller':
                fecha = '2024-03-21'
                df_ventas = df_sc
                df_predict = df_pred_sc

            fecha_sep = pd.to_datetime(fecha)
            fecha_start = fecha_sep - timedelta(6)  # 2024-03-06 (TB) o 2024-03-15 (SCHILLER)
            fecha_fin = fecha_sep + timedelta(7)    # 2024-03-19 (TB) o 2024-03-28 (SCHILLER)
            
            df_ventas = df_ventas[(df_ventas['maquina'] == maq) & (df_ventas['categoria'] == cat) & (df_ventas['producto'] == prod)]
            df_ventas = df_ventas[(df_ventas['fecha'] >= fecha_start) & (df_ventas['fecha'] <= fecha_sep + timedelta(1))]
            df_ventas = df_ventas.groupby(pd.Grouper(key='fecha', freq='d')).count()
            df_ventas.reset_index(inplace=True)

            df_predict = df_predict[(df_predict['maquina'] == maq) & (df_predict['categoria'] == cat) & (df_predict['producto'] == prod)]
            df_predict = df_predict[(df_predict['fecha'] > fecha_sep) & (df_predict['fecha'] <= fecha_fin)]
            df_predict = df_predict.groupby(pd.Grouper(key='fecha', freq='d')).sum()
            df_predict.reset_index(inplace=True)

            objeto_ventas = {}
            for index, row in df_ventas.iterrows():
                if row['fecha'].weekday() != 6:
                    objeto_ventas[row['fecha'].strftime('%Y-%m-%d')] = str(row['producto'])
            
            objeto_predicciones = {}
            for index, row in df_predict.iterrows():
                if row['fecha'].weekday() != 6:
                    objeto_predicciones[row['fecha'].strftime('%Y-%m-%d')] = str(row['prediccion'])
                    
            respuesta = [{'ubicacion':ubi, 'maquina':maq, 'categoria':cat, 'producto':prod}, objeto_ventas, objeto_predicciones]

            return jsonify(respuesta)
        
    else:
        return "Error in args"
    
### fin codigo prediccion




### codigo segmentacion
## thebridge

@app.route('/api/v1/segmentacion/thebridge/vending', methods=['GET'])
def thebridge_vending():
        with open('./data/vending_thebridge_porID.json', 'r') as prod:
            file = json.load(prod)
            return jsonify(file)

@app.route('/api/v1/segmentacion/thebridge/horario', methods=['GET'])
def thebridge_horario():
        with open('./data/horario_clientes_densidad_thebridge.json', 'r') as prod:
            file = json.load(prod)
            return jsonify(file)

@app.route('/api/v1/segmentacion/thebridge/volumen', methods=['GET'])
def thebridge_volumen():
        with open('./data/volumen_compras_horarias_bridge.json', 'r') as prod:
            file = json.load(prod)
            return jsonify(file)

@app.route('/api/v1/segmentacion/thebridge/top', methods=['GET'])
def thebridge_top():
        with open('./data/top3_ventas_bridge.json', 'r') as prod:
            file = json.load(prod)
            return jsonify(file)

@app.route('/api/v1/segmentacion/thebridge/descripcion', methods=['GET'])
def thebridge_descripcion():
        with open('./data/descripcion_cluster_bridge.json', 'r') as prod:
            file = json.load(prod)
            return jsonify(file)

## schiller

@app.route('/api/v1/segmentacion/schiller/vending', methods=['GET'])
def schiller_vending():
        with open('./data/vending_schiller_porID.json', 'r') as prod:
            file = json.load(prod)
            return jsonify(file)

@app.route('/api/v1/segmentacion/schiller/horario', methods=['GET'])
def schiller_horario():
        with open('./data/horario_clientes_densidad_schiller.json', 'r') as prod:
            file = json.load(prod)
            return jsonify(file)

@app.route('/api/v1/segmentacion/schiller/volumen', methods=['GET'])
def schiller_volumen():
        with open('./data/volumen_compras_horarias_schiller.json', 'r') as prod:
            file = json.load(prod)
            return jsonify(file)
        
@app.route('/api/v1/segmentacion/schiller/top', methods=['GET'])
def schiller_top():
        with open('./data/top3_ventas_schiller.json', 'r') as prod:
            file = json.load(prod)
            return jsonify(file)
        
@app.route('/api/v1/segmentacion/schiller/descripcion', methods=['GET'])
def schiller_descripcion():
        with open('./data/descripcion_cluster_schiller.json', 'r') as prod:
            file = json.load(prod)
            return jsonify(file)

### fin codigo segmentacion


### algo mas de codigo prediccion...

# CARGAMOS LA BBDD DE VENTAS (CONSOLIDADO)

df = pd.read_csv('F:/_WORK/DATA SCIENCE/003.THE BRIDGE DS Bootcamp/2 - BOOTCAMP/_entregables Andrada/_Proyecto 04 - Desafío de Tripulaciones/Flask/consolidado.csv', index_col=0)
# df = pd.read_csv('/home/ubuntu/prod/endpoint/consolidado.csv', index_col=0)
df['fecha'] = pd.to_datetime(df['fecha'], format='%Y-%m-%d %H:%M:%S')
df['fecha'] = df['fecha'].dt.date
df['fecha'] = pd.to_datetime(df['fecha'], format='%Y-%m-%d')

df_tb = df[df['ubicacion'] == 'the-bridge']
df_sc = df[df['ubicacion'] == 'schiller']


# CARGAMOS LA BBDD DE PREDICCIONES (PREDICCIONES)

df_pred = pd.read_csv('F:/_WORK/DATA SCIENCE/003.THE BRIDGE DS Bootcamp/2 - BOOTCAMP/_entregables Andrada/_Proyecto 04 - Desafío de Tripulaciones/Flask/predicciones.csv', index_col=0)
# df = pd.read_csv('/home/ubuntu/prod/endpoint/predicciones.csv', index_col=0)
df_pred['fecha'] = pd.to_datetime(df_pred['fecha'], format='%Y-%m-%d')

df_pred_tb = df_pred[df_pred['ubicacion'] == 'the-bridge']
df_pred_sc = df_pred[df_pred['ubicacion'] == 'schiller']

### termina código prediccion...


if __name__ == "__main__":
    app.run(debug=False)
