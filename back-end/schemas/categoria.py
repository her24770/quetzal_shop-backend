from pydantic import BaseModel


# Datos requeridos para crear una categoría
class CategoriaCreate(BaseModel):
    nombre: str
    descripcion: str


# Datos que devuelve la API al consultar una categoría
class CategoriaResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str
