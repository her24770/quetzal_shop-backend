from fastapi import APIRouter, Depends

from schemas.auth import LoginRequest, TokenResponse, UserMe
from dependencies import get_current_user, TokenData
from controllers import auth as auth_controller

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest):
    return auth_controller.login(body.email, body.password)


@router.post("/logout")
def logout():
    return {"message": "Sesión cerrada correctamente"}


@router.get("/me", response_model=UserMe)
def me(current_user: TokenData = Depends(get_current_user)):
    return UserMe(
        user_id=current_user.user_id,
        email=current_user.email,
        rol_id=current_user.rol_id,
        empleado_id=current_user.empleado_id,
    )
