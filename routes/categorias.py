from fastapi import APIRouter, Depends

from schemas.categoria import CategoriaCreate, CategoriaResponse
from dependencies import get_current_user, TokenData
from controllers import categoria as categoria_controller

router = APIRouter()


# GET /categorias — lista todas las categorías
@router.get("/", response_model=list[CategoriaResponse])
def listar(current_user: TokenData = Depends(get_current_user)):
    return categoria_controller.get_all()


# GET /categorias/{id} — obtiene una categoría por ID
@router.get("/{categoria_id}", response_model=CategoriaResponse)
def obtener(categoria_id: int, current_user: TokenData = Depends(get_current_user)):
    return categoria_controller.get_by_id(categoria_id)


# POST /categorias — crea una nueva categoría
@router.post("/", response_model=CategoriaResponse, status_code=201)
def crear(body: CategoriaCreate, current_user: TokenData = Depends(get_current_user)):
    return categoria_controller.create(body)


# DELETE /categorias/{id} — elimina una categoría
@router.delete("/{categoria_id}")
def eliminar(categoria_id: int, current_user: TokenData = Depends(get_current_user)):
    return categoria_controller.delete(categoria_id)
