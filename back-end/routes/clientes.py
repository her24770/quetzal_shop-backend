from fastapi import APIRouter, Depends

from schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse
from dependencies import require_role, TokenData
from controllers import cliente as cliente_controller

router = APIRouter()


# GET /clientes — lista todos los clientes (admin y cajero)
@router.get("/", response_model=list[ClienteResponse])
def listar(current_user: TokenData = Depends(require_role(1, 2))):
    return cliente_controller.get_all()


# GET /clientes/nit/{nit} — busca un cliente por NIT para identificarlo en caja (admin y cajero)
@router.get("/nit/{nit}", response_model=ClienteResponse)
def buscar_por_nit(nit: str, current_user: TokenData = Depends(require_role(1, 2))):
    return cliente_controller.get_by_nit(nit)


# GET /clientes/{id} — obtiene un cliente por ID (admin y cajero)
@router.get("/{cliente_id}", response_model=ClienteResponse)
def obtener(cliente_id: int, current_user: TokenData = Depends(require_role(1, 2))):
    return cliente_controller.get_by_id(cliente_id)


# POST /clientes — registra un nuevo cliente (admin y cajero)
@router.post("/", response_model=ClienteResponse, status_code=201)
def crear(body: ClienteCreate, current_user: TokenData = Depends(require_role(1, 2))):
    return cliente_controller.create(body)


# PATCH /clientes/{id} — actualiza parcialmente un cliente (admin y cajero)
@router.patch("/{cliente_id}", response_model=ClienteResponse)
def actualizar(cliente_id: int, body: ClienteUpdate, current_user: TokenData = Depends(require_role(1, 2))):
    return cliente_controller.update(cliente_id, body)


# DELETE /clientes/{id} — elimina un cliente (solo admin)
@router.delete("/{cliente_id}")
def eliminar(cliente_id: int, current_user: TokenData = Depends(require_role(1))):
    return cliente_controller.delete(cliente_id)
