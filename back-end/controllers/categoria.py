from fastapi import HTTPException, status
from database.queries import categorias as categorias_query
from schemas.categoria import CategoriaCreate, CategoriaUpdate, CategoriaResponse


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


# Actualiza solo los campos que vienen en el body (ignora los None)
def update(categoria_id: int, body: CategoriaUpdate) -> CategoriaResponse:
    campos = {k: v for k, v in body.model_dump().items() if v is not None}
    categoria = categorias_query.update(categoria_id, campos)
    if categoria is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    return categoria


# Elimina una categoría; lanza 404 si no existe y 409 si tiene productos asociados
def delete(categoria_id: int) -> dict:
    try:
        eliminado = categorias_query.delete(categoria_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    if not eliminado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    return {"message": "Categoría eliminada correctamente"}
