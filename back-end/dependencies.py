from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from config import settings

security = HTTPBearer()

class TokenData:
    """Datos extraídos del JWT"""
    def __init__(self, user_id: int, email: str, rol_id: int, empleado_id: int = None):
        self.user_id = user_id
        self.email = email
        self.rol_id = rol_id
        self.empleado_id = empleado_id

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Crea un JWT con los datos proporcionados"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRE_HOURS)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    """
    Extrae y valida el JWT del header Authorization.
    Lanza HTTPException 401 si el token es inválido o expirado.
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: int = payload.get("user_id")
        email: str = payload.get("email")
        rol_id: int = payload.get("rol_id")
        empleado_id: int = payload.get("empleado_id")

        if user_id is None or email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: datos faltantes",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return TokenData(
            user_id=user_id,
            email=email,
            rol_id=rol_id,
            empleado_id=empleado_id
        )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

def require_role(*allowed_roles: int):
    """
    Decorador para verificar que el usuario tiene uno de los roles permitidos.

    Uso:
        @router.get("/admin")
        async def admin_endpoint(current_user: TokenData = Depends(require_role(1))):
            ...
    """
    async def role_checker(current_user: TokenData = Depends(get_current_user)) -> TokenData:
        if current_user.rol_id not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para acceder a este recurso"
            )
        return current_user
    return role_checker
