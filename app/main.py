import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from RetoCoches import diccionario_coches_ultimas_posiciones

# CASO 6
"""
app = FastAPI()

@app.get('/')
def home():
    return diccionario_coches_ultimas_posiciones

@app.get("/{matricula}")
def get_car_info(matricula: str):
    for car_id, car_info in diccionario_coches_ultimas_posiciones.items():
        if car_info["Matricula"] == matricula:
            return car_info
    raise HTTPException(status_code=404, detail="Car not found")

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8080)
"""

# CASO 7
#DATABASE_URL = os.getenv('postgresql://postgres:root@localhost/cochesreto', 'postgresql://postgres:root@localhost/cochesreto')

engine = create_engine('postgresql://postgres:root@localhost/cochesreto',echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

app = FastAPI()

class Coche(Base):
    __tablename__ = 'coches'
    id = Column(Integer, primary_key=True, index=True)
    matricula = Column(String, unique=True, index=True, nullable=False)
    fecha = Column(String, nullable=False)
    latitud = Column(Float, nullable=False)
    longitud = Column(Float, nullable=False)

Base.metadata.create_all(engine)

def cargar_datos():
    with open('ultimaposicion.txt', 'r') as file:
        for line in file:
            partes = line.strip().split(", ")
            matricula = partes[0].split(": ")[1]
            fecha = partes[1].split(": ")[1]
            latitud = float(partes[2].split(": ")[1])
            longitud = float(partes[3].split(": ")[1])
            coche = Coche(matricula=matricula, fecha=fecha, latitud=latitud, longitud=longitud)
            session.add(coche)
        session.commit()
        session.close()

cargar_datos()

# CASO 8

"""
@app.get("/coches/{coche_id}", response_model=Coche)
def read_coche(coche_id: int, db: Session = Depends(Session)):
    db_coche = db.query(Coche).filter(Coche.id == coche_id).first()
    if db_coche is None:
        raise HTTPException(status_code=404, detail="Coche not found")
    return db_coche
"""