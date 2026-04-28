from fastapi import APIRouter, Depends

from schemas.proveedor import ProveedorCreate, ProveedorUpdate, ProveedorResponse
from dependencies import require_role, TokenData
from controllers import proveedor as proveedor_controller

router = APIRouter()


# GET /proveedores — lista todos los proveedores (admin y bodeguero)
@router.get("/", response_model=list[ProveedorResponse])
def listar(current_user: TokenData = Depends(require_role(1, 3))):
    return proveedor_controller.get_all()


# GET /proveedores/{id} — obtiene un proveedor por ID (admin y bodeguero)
@router.get("/{proveedor_id}", response_model=ProveedorResponse)
def obtener(proveedor_id: int, current_user: TokenData = Depends(require_role(1, 3))):
    return proveedor_controller.get_by_id(proveedor_id)


# GET /proveedores/{id}/productos — productos que suministra el proveedor (admin y bodeguero)
@router.get("/{proveedor_id}/productos")
def productos(proveedor_id: int, current_user: TokenData = Depends(require_role(1, 3))):
    return proveedor_controller.get_productos(proveedor_id)


# POST /proveedores — crea un nuevo proveedor (solo admin)
@router.post("/", response_model=ProveedorResponse, status_code=201)
def crear(body: ProveedorCreate, current_user: TokenData = Depends(require_role(1))):
    return proveedor_controller.create(body)


# PATCH /proveedores/{id} — actualiza parcialmente un proveedor (solo admin)
@router.patch("/{proveedor_id}", response_model=ProveedorResponse)
def actualizar(proveedor_id: int, body: ProveedorUpdate, current_user: TokenData = Depends(require_role(1))):
    return proveedor_controller.update(proveedor_id, body)


# DELETE /proveedores/{id} — elimina un proveedor (solo admin)
@router.delete("/{proveedor_id}")
def eliminar(proveedor_id: int, current_user: TokenData = Depends(require_role(1))):
    return proveedor_controller.delete(proveedor_id)
