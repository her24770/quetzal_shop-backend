from fastapi import HTTPException, status
from database.queries import productos as productos_query
from schemas.producto import ProductoCreate, ProductoUpdate, ProductoResponse


# Retorna la lista completa de productos con su categoría
def get_all() -> list[ProductoResponse]:
    return productos_query.get_all()


# Busca un producto por ID y lanza 404 si no existe
def get_by_id(producto_id: int) -> ProductoResponse:
    producto = productos_query.get_by_id(producto_id)
    if producto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return producto


# Retorna productos cuyo stock está en o por debajo del mínimo
def get_stock_bajo() -> list[ProductoResponse]:
    return productos_query.get_stock_bajo()


# Crea un nuevo producto con los datos del body
def create(body: ProductoCreate) -> ProductoResponse:
    return productos_query.create(
        body.nombre,
        body.descripcion,
        body.precio,
        body.stock,
        body.stock_minimo,
        body.categoria_id,
    )


# Actualiza solo los campos que vienen en el body (ignora los None)
def update(producto_id: int, body: ProductoUpdate) -> ProductoResponse:
    campos = {k: v for k, v in body.model_dump().items() if v is not None}
    producto = productos_query.update(producto_id, campos)
    if producto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return producto


# Elimina un producto y lanza 404 si no existía
def delete(producto_id: int) -> dict:
    eliminado = productos_query.delete(producto_id)
    if not eliminado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return {"message": "Producto eliminado correctamente"}
