from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3


app = FastAPI()

class Candidato(BaseModel):
    dni: str
    nombre: str
    apellido: str

conexion = sqlite3.connect('candidatos.db')
cursor = conexion.cursor()

@app.post('/candidato')
async def agregar_candidato(candidato: Candidato):
    #Comprobar si DNI existe en la base de datos
    cursor.execute(f"SELECT * FROM candidatos WHERE dni={candidato.dni}")
    existing_candidato = cursor.fetchone()
    if existing_candidato:
        raise HTTPException(status_code=400, detail="El candidato ya exite")
    
    #Si no existe el canditado lo añadimos
    cursor.execute(f"INSERT INTO candidatos VALUES ({candidato.dni}, {candidato.nombre},{candidato.apellido})")
    conexion.commit()

    return {"mensaje":"Canditado agregado correctamente"}

#Cerrar la conexion a la base de datos cuando se apague el servidor
@app.on_event("shutdown")
def shutdown_event():
    conexion.close()