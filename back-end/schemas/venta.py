from pydantic import BaseModel
from typing import Optional


# Un item que el cliente está comprando
class ItemVentaCreate(BaseModel):
    producto_id: int
    cantidad: int


# Datos que manda el cajero al registrar una venta
# El empleado_id viene del JWT, no del body
class VentaCreate(BaseModel):
    cliente_id: int
    metodo_pago_id: int
    descuento: float = 0.0
    items: list[ItemVentaCreate]


# Detalle de un item en la respuesta de la venta
class ItemVentaResponse(BaseModel):
    producto_id: int
    producto_nombre: str
    cantidad: int
    precio_unitario_historico: float
    subtotal: float


# Respuesta completa de una venta con sus items
class VentaResponse(BaseModel):
    id: int
    cliente_id: int
    cliente_nombre: str
    empleado_id: int
    empleado_nombre: str
    metodo_pago_id: int
    metodo_pago: str
    fecha: str
    total: float
    descuento: float
    items: list[ItemVentaResponse]


# Respuesta resumida para el listado general de ventas
class VentaResumen(BaseModel):
    id: int
    fecha: str
    total: float
    descuento: float
    cliente: str
    nit: str
    empleado: str
    metodo_pago: str
