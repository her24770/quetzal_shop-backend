from fastapi import HTTPException, status
from database.queries import clientes as clientes_query
from schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse


# Retorna la lista completa de clientes
def get_all() -> list[ClienteResponse]:
    return clientes_query.get_all()


# Busca un cliente por ID y lanza 404 si no existe
def get_by_id(cliente_id: int) -> ClienteResponse:
    cliente = clientes_query.get_by_id(cliente_id)
    if cliente is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return cliente


# Busca un cliente por NIT y lanza 404 si no existe
def get_by_nit(nit: str) -> ClienteResponse:
    cliente = clientes_query.get_by_nit(nit)
    if cliente is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return cliente


# Crea un nuevo cliente con los datos del body
def create(body: ClienteCreate) -> ClienteResponse:
    return clientes_query.create(body.nombre, body.nit, body.telefono, body.direccion)


# Actualiza solo los campos que vienen en el body (ignora los None)
def update(cliente_id: int, body: ClienteUpdate) -> ClienteResponse:
    campos = {k: v for k, v in body.model_dump().items() if v is not None}
    cliente = clientes_query.update(cliente_id, campos)
    if cliente is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return cliente


# Elimina un cliente y lanza 404 si no existía
def delete(cliente_id: int) -> dict:
    eliminado = clientes_query.delete(cliente_id)
    if not eliminado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return {"message": "Cliente eliminado correctamente"}
