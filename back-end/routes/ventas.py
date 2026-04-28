from fastapi import APIRouter, Depends

from schemas.venta import VentaCreate, VentaResponse, VentaResumen
from dependencies import require_role, TokenData
from controllers import venta as venta_controller

router = APIRouter()


# GET /ventas — lista todas las ventas resumidas (admin y cajero)
@router.get("/", response_model=list[VentaResumen])
def listar(current_user: TokenData = Depends(require_role(1, 2))):
    return venta_controller.get_all()


# GET /ventas/metodos-pago — lista los métodos de pago disponibles (admin y cajero)
@router.get("/metodos-pago")
def metodos_pago(current_user: TokenData = Depends(require_role(1, 2))):
    return venta_controller.get_metodos_pago()


# GET /ventas/{id} — obtiene una venta completa con sus items (admin y cajero)
@router.get("/{venta_id}", response_model=VentaResponse)
def obtener(venta_id: int, current_user: TokenData = Depends(require_role(1, 2))):
    return venta_controller.get_by_id(venta_id)


# POST /ventas — registra una nueva venta con transacción (admin y cajero)
# El empleado_id se toma del token para saber quién realizó la venta
@router.post("/", response_model=VentaResponse, status_code=201)
def crear(body: VentaCreate, current_user: TokenData = Depends(require_role(1, 2))):
    return venta_controller.crear(body, current_user.empleado_id)
