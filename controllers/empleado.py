from fastapi import HTTPException, status
from database.queries import empleados as empleados_query
from schemas.empleado import EmpleadoCreate, EmpleadoUpdate, EmpleadoResponse


# Retorna la lista completa de empleados con su email y rol
def get_all() -> list[EmpleadoResponse]:
    return empleados_query.get_all()


# Busca un empleado por ID y lanza 404 si no existe
def get_by_id(empleado_id: int) -> EmpleadoResponse:
    empleado = empleados_query.get_by_id(empleado_id)
    if empleado is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empleado no encontrado")
    return empleado


# Crea un nuevo empleado con los datos del body
def create(body: EmpleadoCreate) -> EmpleadoResponse:
    return empleados_query.create(
        body.usuario_id,
        body.dpi,
        body.nombre,
        body.telefono,
        body.cargo,
        body.fecha_contrato,
    )


# Actualiza solo los campos que vienen en el body (solo telefono, cargo y estado son editables)
def update(empleado_id: int, body: EmpleadoUpdate) -> EmpleadoResponse:
    campos = {k: v for k, v in body.model_dump().items() if v is not None}
    empleado = empleados_query.update(empleado_id, campos)
    if empleado is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empleado no encontrado")
    return empleado


# Elimina un empleado y lanza 404 si no existía
def delete(empleado_id: int) -> dict:
    eliminado = empleados_query.delete(empleado_id)
    if not eliminado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empleado no encontrado")
    return {"message": "Empleado eliminado correctamente"}
