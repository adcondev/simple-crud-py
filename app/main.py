# Aplicación principal FastAPI
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core import config
from app.db.session import create_tables, ping_database
from app.api.endpoints import books


# Ciclo de vida de la aplicación
@asynccontextmanager
async def lifespan(api: FastAPI):
    # Startup - Configurar DB y tablas
    print(f"🚀 Iniciando API en modo {config.settings.ENVIRONMENT}")
    create_tables()
    print("📚 API lista para recibir solicitudes")
    yield
    # Shutdown
    print("👋 Aplicación finalizada")


# Configuración de la aplicación FastAPI
app = FastAPI(
    title="Simple CRUD FastAPI",
    description="API para gestión de libros con PostgreSQL",
    version="1.0.0",
    docs_url="/docs",    # Swagger UI
    redoc_url="/redoc",  # Documentación alternativa
    lifespan=lifespan
)

# Registrar endpoints de libros
app.include_router(books.router)


# Endpoints básicos de la API
@app.get("/")
async def root():
    """Información de bienvenida"""
    return {
        "message": "¡Bienvenido a Simple CRUD API de Libros!",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {"books": "/books"}
    }


@app.get("/health")
async def health_check():
    """Estado de la API y base de datos"""
    db_status = ping_database()
    return {
        "status": "healthy" if db_status else "unhealthy",
        "database": "connected" if db_status else "disconnected",
        "environment": config.settings.ENVIRONMENT
    }


@app.get("/info")
async def api_info():
    """Metadatos detallados de la API"""
    return {
        "name": "Simple CRUD FastAPI",
        "description": "API REST para gestión de libros",
        "version": "1.0.0",
        "features": [
            "CRUD completo para libros",
            "Búsqueda por autor",
            "Documentación automática",
            "Base de datos PostgreSQL"
        ],
        "endpoints_count": {"books": 6}
    }
