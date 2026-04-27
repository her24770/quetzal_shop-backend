from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import auth

# ---------------------------------------------------------------------------
# Inicialización de la aplicación FastAPI
# ---------------------------------------------------------------------------
app = FastAPI(
    title="QuetzalShop API",
    description="Backend del sistema POS QuetzalShop",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# CORS — permite que el frontend (SvelteKit o React) haga requests al backend.
# En producción esto debería restringirse al dominio real.
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # SvelteKit dev
        "http://localhost:3000",  # alternativo
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Registro de routers
# Cada módulo de routes/ se agrega aquí con su prefijo y etiqueta.
# En ramas futuras se irán sumando: productos, ventas, compras, etc.
# ---------------------------------------------------------------------------
app.include_router(auth.router, prefix="/auth", tags=["Autenticación"])


# ---------------------------------------------------------------------------
# Endpoint raíz — útil para verificar que el servidor está vivo
# ---------------------------------------------------------------------------
@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "app": "QuetzalShop API"}
