from datetime import timedelta
from fastapi import HTTPException, status
from passlib.context import CryptContext

from schemas.auth import TokenResponse, UserInfo
from database.queries.auth import get_user_by_email
from dependencies import create_access_token
from config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def login(email: str, password: str) -> TokenResponse:
    user = get_user_by_email(email)

    if user is None or not pwd_context.verify(password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_payload = {
        "user_id":     user["user_id"],
        "email":       user["email"],
        "rol_id":      user["rol_id"],
        "empleado_id": user["empleado_id"],
    }

    token = create_access_token(
        data=token_payload,
        expires_delta=timedelta(hours=settings.JWT_EXPIRE_HOURS)
    )

    return TokenResponse(
        access_token=token,
        user=UserInfo(
            user_id=user["user_id"],
            email=user["email"],
            rol_id=user["rol_id"],
            rol_nombre=user["rol_nombre"],
            empleado_id=user["empleado_id"],
            nombre_empleado=user["nombre_empleado"],
        )
    )
