from fastapi import HTTPException, status
from database.queries import proveedores as proveedores_query
from schemas.proveedor import ProveedorCreate, ProveedorUpdate, ProveedorResponse


# Retorna la lista completa de proveedores
def get_all() -> list[ProveedorResponse]:
    return proveedores_query.get_all()


# Busca un proveedor por ID y lanza 404 si no existe
def get_by_id(proveedor_id: int) -> ProveedorResponse:
    proveedor = proveedores_query.get_by_id(proveedor_id)
    if proveedor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado")
    return proveedor


# Retorna los productos que suministra un proveedor con sus precios de costo
def get_productos(proveedor_id: int) -> list:
    get_by_id(proveedor_id)
    return proveedores_query.get_productos(proveedor_id)


# Crea un nuevo proveedor con los datos del body
def create(body: ProveedorCreate) -> ProveedorResponse:
    return proveedores_query.create(body.nombre, body.telefono, body.email, body.direccion)


# Actualiza solo los campos que vienen en el body (ignora los None)
def update(proveedor_id: int, body: ProveedorUpdate) -> ProveedorResponse:
    campos = {k: v for k, v in body.model_dump().items() if v is not None}
    proveedor = proveedores_query.update(proveedor_id, campos)
    if proveedor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado")
    return proveedor


# Elimina un proveedor y lanza 404 si no existía
def delete(proveedor_id: int) -> dict:
    eliminado = proveedores_query.delete(proveedor_id)
    if not eliminado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado")
    return {"message": "Proveedor eliminado correctamente"}
