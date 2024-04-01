from flask import Flask, request, jsonify
from flask_cors import CORS

import pandas as pd
import numpy as np
import datetime as dt
from datetime import datetime, timedelta


### para segmentacion
import json
### fin import segmentacion



# ==============================================================================================================================
# Funcion que me sirve en todos los endpoints de 3 a 6
# ==============================================================================================================================

def carga_seleccion_datos(ubi):

    if ubi == 'the-bridge':
        fecha = '2024-03-12'
        df_ventas = df_tb
        df_predict = df_pred_tb
        objeto_ventas =   {
                            "2024-03-06": "0",
                            "2024-03-07": "0",
                            "2024-03-08": "0",
                            "2024-03-09": "0",
                            "2024-03-11": "0",
                            "2024-03-12": "0"
        }
        objeto_predicciones =   {
                                "2024-03-13": "0",
                                "2024-03-14": "0",
                                "2024-03-15": "0",
                                "2024-03-16": "0",
                                "2024-03-18": "0",
                                "2024-03-19": "0"
                            }
    elif ubi == 'schiller':
        fecha = '2024-03-21'
        df_ventas = df_sc
        df_predict = df_pred_sc
        objeto_ventas =   {
                            "2024-03-15": "0",
                            "2024-03-16": "0",
                            "2024-03-18": "0",
                            "2024-03-19": "0",
                            "2024-03-20": "0",
                            "2024-03-21": "0"
        }
        objeto_predicciones =   {
                                "2024-03-22": "0",
                                "2024-03-23": "0",
                                "2024-03-25": "0",
                                "2024-03-26": "0",
                                "2024-03-27": "0",
                                "2024-03-28": "0"
                            }

    return fecha, df_ventas, df_predict, objeto_ventas, objeto_predicciones




#===============================================================================================================================
# Endpoint HOME 
#==============================================================================================================================

@app.route('/', methods=['GET'])
def home():
    return "<h1>3_Prueba Desafío PREDICCION DE VENTAS</h1>"



# ==============================================================================================================================
# ENDPOINT 1 - FACTURACION   --> ( Los datos los pasamos por la URL ) [GET] )
# ==============================================================================================================================

"""
La petición sería tipo:

http://127.0.0.1:5000/api/v1/ventas/general/facturacion?ubicacion=the-bridge
o
http://127.0.0.1:5000/api/v1/ventas/general/facturacion?ubicacion=schiller

"""

@app.route('/api/v1/ventas/general/facturacion', methods = ['GET']) 
def facturacion():

    args = request.args
    if 'ubicacion' in args:

        ubi = args.get('ubicacion', None)

        if ubi not in list(df['ubicacion'].unique()):
            return "Error. Incorrect arguments"
        else:

            if ubi == 'the-bridge':
                respuesta = {'corner': 'the-bridge',
                            'total diario': [45, -57],
                            'total semanal': [149, -73],
                            'total mensual': [826, -57]}
            elif ubi == 'schiller':
                respuesta = {'corner': 'schiller',
                            'total diario': [3, -98],
                            'total semanal': [431, -27],
                            'total mensual': [1830, -42]}

            return jsonify(respuesta)
        
    else:
        return "Error in args"




# ==============================================================================================================================
# ENDPOINT 2 - PRODUCTOS DESTACADOS   --> ( Los datos los pasamos por la URL ) [GET] )
# ==============================================================================================================================

"""
La petición sería tipo:

http://127.0.0.1:5000/api/v1/ventas/general/productosdestacados?ubicacion=the-bridge
o
http://127.0.0.1:5000/api/v1/ventas/general/productosdestacados?ubicacion=schiller

"""

@app.route('/api/v1/ventas/general/productosdestacados', methods = ['GET']) 
def productos_destacados():

    args = request.args
    if 'ubicacion' in args:

        ubi = args.get('ubicacion', None)

        if ubi not in list(df['ubicacion'].unique()):
            return "Error. Incorrect arguments"
        else:

            if ubi == 'the-bridge':
                respuesta = {'producto_mas_vendido': {'producto': 'pincho-de-tortilla-patatas', 'porcentaje': 566.7, 'unidades': 1.7},
                              'producto_menos_vendido': {'producto': 'cafe-con-leche', 'porcentaje': -45.6, 'unidades': -31.9},
                              'producto_estrella': {'producto': 'cafe-con-leche', 'porcentaje': 699.0, 'unidades': -57}}
            elif ubi == 'schiller':
                respuesta = {'producto_mas_vendido': {'producto': 'mios-maiz', 'porcentaje': 411.4, 'unidades': 7.2},
                              'producto_menos_vendido': {'producto': 'cafe-con-leche', 'porcentaje': -70.6, 'unidades': -28.8},
                              'producto_estrella': {'producto': 'cafe-con-leche', 'porcentaje': 1195.0, 'unidades': -24}}


            return jsonify(respuesta)
        
    else:
        return "Error in args"



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
def analitica_general():

    args = request.args
    if 'ubicacion' in args:

        ubi = args.get('ubicacion', None)

        if ubi not in list(df['ubicacion'].unique()):
            return "Error. Incorrect arguments"
        else:

            fecha, df_ventas, df_predict, objeto_ventas, objeto_predicciones = carga_seleccion_datos(ubi)

            fecha_sep = pd.to_datetime(fecha)
            fecha_start = fecha_sep - timedelta(6)  # 2024-03-06 (TB) o 2024-03-15 (SCHILLER)
            fecha_fin = fecha_sep + timedelta(7)    # 2024-03-19 (TB) o 2024-03-28 (SCHILLER)

            df_ventas = df_ventas[(df_ventas['fecha'] >= fecha_start) & (df_ventas['fecha'] <= fecha_sep + timedelta(1))]
            df_ventas = df_ventas.groupby(pd.Grouper(key='fecha', freq='d')).count()
            df_ventas.reset_index(inplace=True)                

            df_predict = df_predict[(df_predict['fecha'] > fecha_sep) & (df_predict['fecha'] <= fecha_fin)]
            df_predict = df_predict.groupby(pd.Grouper(key='fecha', freq='d')).sum()
            df_predict.reset_index(inplace=True)

            for index, row in df_ventas.iterrows():
                if row['fecha'].weekday() != 6:
                    objeto_ventas[row['fecha'].strftime('%Y-%m-%d')] = str(row['producto'])
            
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
def analitica_por_maquina():

    args = request.args
    if ('ubicacion' in args) and ('maquina' in args):

        ubi = args.get('ubicacion', None)
        maq = args.get('maquina', None)

        if ubi in list(df['ubicacion'].unique()):

            df_1 = df[df['ubicacion'] == ubi]
            if maq in list(df_1['maquina'].unique()):
            
                fecha, df_ventas, df_predict, objeto_ventas, objeto_predicciones = carga_seleccion_datos(ubi)

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

                for index, row in df_ventas.iterrows():
                    if row['fecha'].weekday() != 6:
                        objeto_ventas[row['fecha'].strftime('%Y-%m-%d')] = str(row['producto'])
                
                for index, row in df_predict.iterrows():
                    if row['fecha'].weekday() != 6:
                        objeto_predicciones[row['fecha'].strftime('%Y-%m-%d')] = str(row['prediccion'])
                        
                respuesta = [{'ubicacion':ubi, 'maquina':maq}, objeto_ventas, objeto_predicciones]

                return jsonify(respuesta)
            
            else:
                return "Error. Incorrect arguments"
        else:
                return "Error. Incorrect arguments"
        
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
def analitica_por_categoria():

    args = request.args
    if ('ubicacion' in args) and ('maquina' in args) and ('categoria' in args):

        ubi = args.get('ubicacion', None)
        maq = args.get('maquina', None)
        cat = args.get('categoria', None)

        if ubi in list(df['ubicacion'].unique()):

            df_1 = df[df['ubicacion'] == ubi]
            if maq in list(df_1['maquina'].unique()):

                df_2 = df_1[df_1['maquina'] == maq]
                if cat in list(df_2['categoria'].unique()):
                    
                    fecha, df_ventas, df_predict, objeto_ventas, objeto_predicciones = carga_seleccion_datos(ubi)

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

                    for index, row in df_ventas.iterrows():
                        if row['fecha'].weekday() != 6:
                            objeto_ventas[row['fecha'].strftime('%Y-%m-%d')] = str(row['producto'])

                    for index, row in df_predict.iterrows():
                        if row['fecha'].weekday() != 6:
                            objeto_predicciones[row['fecha'].strftime('%Y-%m-%d')] = str(row['prediccion'])
                            
                    respuesta = [{'ubicacion':ubi, 'maquina':maq, 'categoria':cat}, objeto_ventas, objeto_predicciones]

                    return jsonify(respuesta)
                
                else:
                    return "Error. Incorrect arguments"
            else:
                return "Error. Incorrect arguments"
        else:
            return "Error. Incorrect arguments"

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
def analitica_por_producto():

    args = request.args
    if ('ubicacion' in args) and ('maquina' in args) and ('categoria' in args) and ('producto' in args):

        ubi = args.get('ubicacion', None)
        maq = args.get('maquina', None)
        cat = args.get('categoria', None)
        prod = args.get('producto', None)

        if ubi in list(df['ubicacion'].unique()):

            df_1 = df[df['ubicacion'] == ubi]
            if maq in list(df_1['maquina'].unique()):

                df_2 = df_1[df_1['maquina'] == maq]
                if cat in list(df_2['categoria'].unique()):

                    df_3 = df_2[df_2['categoria'] == cat]
                    if prod in list(df_3['producto'].unique()):

                        fecha, df_ventas, df_predict, objeto_ventas, objeto_predicciones = carga_seleccion_datos(ubi)

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

                        for index, row in df_ventas.iterrows():
                            if row['fecha'].weekday() != 6:
                                objeto_ventas[row['fecha'].strftime('%Y-%m-%d')] = str(row['producto'])

                        for index, row in df_predict.iterrows():
                            if row['fecha'].weekday() != 6:
                                objeto_predicciones[row['fecha'].strftime('%Y-%m-%d')] = str(row['prediccion'])
                                
                        respuesta = [{'ubicacion':ubi, 'maquina':maq, 'categoria':cat, 'producto':prod}, objeto_ventas, objeto_predicciones]

                        return jsonify(respuesta)

                    else:
                        return "Error. Incorrect arguments"
                else:
                    return "Error. Incorrect arguments"
            else:
                return "Error. Incorrect arguments"
        else:
            return "Error. Incorrect arguments"
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

df = pd.read_csv('./data/consolidado.csv', index_col=0)
# df = pd.read_csv('/home/ubuntu/prod/endpoint/consolidado.csv', index_col=0)
df['fecha'] = pd.to_datetime(df['fecha'], format='%Y-%m-%d %H:%M:%S')
df['fecha'] = df['fecha'].dt.date
df['fecha'] = pd.to_datetime(df['fecha'], format='%Y-%m-%d')

df_tb = df[df['ubicacion'] == 'the-bridge']
df_sc = df[df['ubicacion'] == 'schiller']


# CARGAMOS LA BBDD DE PREDICCIONES (PREDICCIONES)

df_pred = pd.read_csv('./data/predicciones.csv', index_col=0)
# df = pd.read_csv('/home/ubuntu/prod/endpoint/predicciones.csv', index_col=0)
df_pred['fecha'] = pd.to_datetime(df_pred['fecha'], format='%Y-%m-%d')

df_pred_tb = df_pred[df_pred['ubicacion'] == 'the-bridge']
df_pred_sc = df_pred[df_pred['ubicacion'] == 'schiller']

### termina código prediccion...


if __name__ == "__main__":
    app.run(debug=False)
