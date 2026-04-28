from pydantic import BaseModel, EmailStr
from typing import Optional


# Lo que el usuario manda al hacer login
class LoginRequest(BaseModel):
    email: str
    password: str


# Datos básicos del usuario que se incluyen en la respuesta de login y en /me.
# Combina info de la tabla usuarios, roles y empleados (si tiene empleado).
class UserInfo(BaseModel):
    user_id: int
    email: str
    rol_id: int
    rol_nombre: str
    empleado_id: Optional[int] = None
    nombre_empleado: Optional[str] = None


# Respuesta completa del login:
# devuelve el token JWT y los datos del usuario para el frontend
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserInfo


# Lo que devuelve GET /auth/me — los datos del usuario actualmente logueado
class UserMe(BaseModel):
    user_id: int
    email: str
    rol_id: int
    empleado_id: Optional[int] = None
