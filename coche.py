from typing import Optional
from xmlrpc.client import DateTime

from pydantic import BaseModel

class Coche(BaseModel):
    matricula: str
    latitud: float
    longitud: float
    pos_date: DateTime