from pydantic import BaseModel
from typing import Optional


# Datos requeridos para crear un cliente
class ClienteCreate(BaseModel):
    nombre: str
    nit: str
    telefono: str
    direccion: str


# Todos los campos son opcionales para permitir edición parcial (PATCH)
class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    nit: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None


# Datos que devuelve la API al consultar un cliente
class ClienteResponse(BaseModel):
    id: int
    nombre: str
    nit: str
    telefono: str
    direccion: str
