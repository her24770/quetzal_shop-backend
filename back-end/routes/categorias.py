from fastapi import APIRouter, Depends

from schemas.categoria import CategoriaCreate, CategoriaResponse
from dependencies import require_role, TokenData
from controllers import categoria as categoria_controller

router = APIRouter()


# GET /categorias — lista todas las categorías (todos los roles)
@router.get("/", response_model=list[CategoriaResponse])
def listar(current_user: TokenData = Depends(require_role(1, 2, 3))):
    return categoria_controller.get_all()


# GET /categorias/{id} — obtiene una categoría por ID (todos los roles)
@router.get("/{categoria_id}", response_model=CategoriaResponse)
def obtener(categoria_id: int, current_user: TokenData = Depends(require_role(1, 2, 3))):
    return categoria_controller.get_by_id(categoria_id)


# POST /categorias — crea una nueva categoría (solo admin)
@router.post("/", response_model=CategoriaResponse, status_code=201)
def crear(body: CategoriaCreate, current_user: TokenData = Depends(require_role(1))):
    return categoria_controller.create(body)


# DELETE /categorias/{id} — elimina una categoría (solo admin)
@router.delete("/{categoria_id}")
def eliminar(categoria_id: int, current_user: TokenData = Depends(require_role(1))):
    return categoria_controller.delete(categoria_id)
