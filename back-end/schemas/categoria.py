from pydantic import BaseModel
from typing import Optional


# Datos requeridos para crear una categoría
class CategoriaCreate(BaseModel):
    nombre: str
    descripcion: str


# Todos los campos son opcionales para edición parcial (PATCH)
class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None


# Datos que devuelve la API al consultar una categoría
class CategoriaResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str
