from typing import Dict, List, Optional
from fastapi import FastAPI
from joblib import load
from tinydb import TinyDB, Query
from datetime import datetime
from tinydb.operations import set
import numpy as np

app = FastAPI(title = "Lab 10")

# aquí carguen el modelo guardado (con load de joblib) y
model = load('modelo.joblib')
# el cliente de base de datos (con tinydb). Usen './db.json' como bbdd.
db = TinyDB("./db.json")

# Nota: En el caso que al guardar en la bbdd les salga una excepción del estilo JSONSerializable
# conviertan el tipo de dato a uno más sencillo.
# Por ejemplo, si al guardar la predicción les levanta este error, usen int(prediccion[0])
# para convertirla a un entero nativo de python.

# Nota 2: Las funciones ya están implementadas con todos sus parámetros. No deberían
# agregar más que esos.


@app.get('/')
async def home():
    return {'message': 'Buenas!! Esta es una API generada con FAST API :D'}

@app.post("/potabilidad/")
async def predict_and_save(observation: Dict[str, float]):
    # implementar 1. aquí

    current_time = datetime.now() # right here, right now

    array = np.array([value for value in observation.values()], ndmin = 2) # array con los datos

    # generamos predicción
    prediction = model.predict(array)[0]

    # updateamos diccionario
    observation.update({
        'Day': int(current_time.day), 'Month': int(current_time.month), 
        'Year': int(current_time.year), 'Prediction': int(prediction),
        })

    response = {'potabilidad': prediction.tolist(), 'id': db.insert(observation)}
    return response

@app.get("/potabilidad/")
async def read_all():
    # implementar 2 aquí.
    return db.all() # retornamos todas las mediciones guardadas, nos toma solo una linea :p


@app.get("/potabilidad_diaria/")
async def read_by_day(day: int, month: int, year: int):
    # implementar 3 aquí
    query = Query()

    return db.search((query.Day == day) & (query.Month <= month) & (query.Year == year))


@app.put("/potabilidad/")
async def update_by_day(day: int, month: int, year: int, new_prediction: int):
    # implementar 4 aquí
    query = Query()
    
    try:
        # en caso de ejecutarse correctamente, actualizamos elementos y devolvemos True
        return {'success': True, 'updated_elements': db.update(set("Prediction", new_prediction), (query.Day == day) & 
                                                    (query.Month <= month) & (query.Year == year))}
    except:
        # en caso contrario, devolvemos False
        return {'success': False, 'updated_elements': 'No pude actualizar ningún elemento :('}


@app.delete("/potabilidad/")
async def delete_by_day(day: int, month: int, year: int):
    # implementar 5 aquí
    query = Query()

    try:
        # en caso de ejecutarse correctamente, eliminamos elementos y devolvemos True
        return {'success': True, 'deleted_elements': db.remove((query.Day == day) & (query.Month <= month) & (query.Year == year))}
    except:
        # en caso contrario, devolvemos False
        return {'success': False, 'deteled_elements': 'No pude eliminar ningún elemento :('}