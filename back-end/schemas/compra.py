from pydantic import BaseModel


# Un item de la compra con su proveedor y precio de costo
class ItemCompraCreate(BaseModel):
    producto_id: int
    proveedor_id: int
    cantidad: int
    precio_costo: float


# Datos que manda el bodeguero al registrar una compra
# El empleado_id viene del JWT, no del body
class CompraCreate(BaseModel):
    numero_factura: str
    items: list[ItemCompraCreate]


# Detalle de un item en la respuesta de la compra
class ItemCompraResponse(BaseModel):
    producto_id: int
    producto_nombre: str
    proveedor_id: int
    proveedor_nombre: str
    cantidad: int
    precio_costo_historico: float
    subtotal: float


# Respuesta completa de una compra con sus items
class CompraResponse(BaseModel):
    id: int
    empleado_id: int
    empleado_nombre: str
    fecha: str
    total: float
    numero_factura: str
    items: list[ItemCompraResponse]


# Respuesta resumida para el listado general de compras
class CompraResumen(BaseModel):
    id: int
    fecha: str
    total: float
    numero_factura: str
    empleado: str
