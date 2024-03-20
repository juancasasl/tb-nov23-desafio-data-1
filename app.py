#==============================================================================================================================
# ESTE ES EL CUERPO DE LA APP 
# AQUI SE DEFINEN LAS DISTINTAS ESTANCIAS DE LAS APP WEB 
# ACCIONES QUE SE REALIZARÁN EN LAS ESTANCIAS DEFINIDAS:
#    
#    1.Implementacion de modelos de Prediccion elegidos  y visualizacion de su scoring:
#                                                       a.Prediccion 1 mediante Regresion Lineal o similar 
#                                                       b.Prediccion 2 mediante XXX
#                                                       c.Prediccion 3 mediante XXX
#
#    En el proceso de implementacion se tienen que emplear 3 maneras para suministrar los datos al modelo   
#     1. A traves de la URL(http) de manera manual  (opcion request de flask )        
#     2. A traves de un paquete de datos json que estara en un tercer script que llamaremos ataque (opcion requests de peticiones)
#     3. A traves de una ruta que acepte ambos (habría que pensarla un poco)
#===============================================================================================================================

from flask import Flask, request, jsonify
import pickle
import pandas as pd
import numpy as np
import csv, sqlite3, json
from sklearn.model_selection import train_test_split  #Aquí no se hace un train test split 
from sklearn.metrics import mean_squared_error        #Empleo el modelo que aplique 
from sklearn.linear_model import LinearRegression     #Empleo el modelo que aplique 

app = Flask(__name__)
app.config["DEBUG"] = True



# ==============================================================================================================================
# [1] PREDICCION  1 --> ( Empleamos solo 1 modelo. Los datos los pasamos por la URL )
# ==============================================================================================================================

"""
La petición sería:
http://13.51.194.81/api/v1/adv_model/predict?param1=THEBRIDGE&param2=MAQUINA2&param3=PRODUCTOCOCACOLA&paramFECHA:20-03-2024   #Esta ruta la definimos nosotros así
"""

@app.route('/api/v1/segmentacion', methods = ['GET'])  #['GET']: Aquí coge los argumentos por param1,param2 y param3 por URL con 'request.arg'
def predict():
    args = request.args
    if 'param1' in args and 'param2' in args and 'param3' in args and 'param4' in args:
        with open('/home/ubuntu/prod/endpoint/lr_model.pkl','rb') as archivo_entrada : 
            model = pickle.load(archivo_entrada) # Modelo cargado
        
        parametro1 = args.get('param1', None) #Coge lo que le pasas por el parametro 1 y sino coge 'None'
        parametro2 = args.get('param2', None)
        parametro3 = args.get('param3', None)
        parametro4 = args.get('param4', None)

        if parametro1 is None or parametro2 is None or parametro3 is None or parametro4 is None:
            return "Error. Args empty"
        else:
            predictions = model.predict([[(parametro1), (parametro2), (parametro3), float(parametro4)]]) # Cambiar el float por el tipo que sean los parámetros
            return jsonify({"predictions": list(predictions)})
    else:
        return "Error in args"

# Aquí estamos haciendo la predicciones, las metricas de nuestro modelo las ponemos a parte en otra @app.route 
    


# comment out all app.run

# if __name__ == "__main__":
#     print("hello")
#     app.run(debug=False)


# app.run()
