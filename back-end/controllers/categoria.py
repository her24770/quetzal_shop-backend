from fastapi import HTTPException, status
from database.queries import categorias as categorias_query
from schemas.categoria import CategoriaCreate, CategoriaResponse


# Retorna la lista completa de categorías
def get_all() -> list[CategoriaResponse]:
    return categorias_query.get_all()


# Busca una categoría por ID y lanza 404 si no existe
def get_by_id(categoria_id: int) -> CategoriaResponse:
    categoria = categorias_query.get_by_id(categoria_id)
    if categoria is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    return categoria


# Crea una nueva categoría con los datos del body
def create(body: CategoriaCreate) -> CategoriaResponse:
    return categorias_query.create(body.nombre, body.descripcion)


# Elimina una categoría y lanza 404 si no existía
def delete(categoria_id: int) -> dict:
    eliminado = categorias_query.delete(categoria_id)
    if not eliminado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    return {"message": "Categoría eliminada correctamente"}
