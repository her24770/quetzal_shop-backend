from pydantic import BaseModel
from typing import Optional


# Datos requeridos para crear un proveedor
class ProveedorCreate(BaseModel):
    nombre: str
    telefono: str
    email: str
    direccion: str


# Todos los campos son opcionales para permitir edición parcial (PATCH)
class ProveedorUpdate(BaseModel):
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None


# Datos que devuelve la API al consultar un proveedor
class ProveedorResponse(BaseModel):
    id: int
    nombre: str
    telefono: str
    email: str
    direccion: str
