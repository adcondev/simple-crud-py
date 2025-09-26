from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core import config
from app.db.session import create_tables, ping_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Hacer antes del startup de la aplicación
    print(f"🚀 Aplicación iniciada en modo {config.settings.ENVIRONMENT}")
    print(f"🔗 Conectado a base de datos: {config.settings.DB_HOST}")
    create_tables()
    # Correr la aplicación
    yield
    # Shutdown de la aplicación
    print("👋 Aplicación finalizada")


app = FastAPI(
    title="Simple CRUD FastAPI",
    description="Una API simple para aprender FastAPI con PostgreSQL",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)


# app es la instancia principal de FastAPI
# El decorador(@) indica el endpoint("/") y el métoodo HTTP(.get)
# async indica que la función es asíncrona, es decir, puede manejar múltiples solicitudes al mismo tiempo
# No te preocupes por lo pronto, Concurrencia es un tema avanzado
# Un decorador es un tipo de sandwich:
# def get(func):
#     def wrapper():
#         print("Hacer algo antes de la función")
#         root()
#         print("Hacer algo después de la función")
#     return wrapper
# Igual de eso se encarga FastAPI
@app.get("/")
async def root():
    """ Endpoint raíz que proporciona información básica sobre la API """
    # Nada extraordinario, solo un mensaje de bienvenida
    return {
        "message": "Simple CRUD con FastAPI, SQLModel y PostgreSQL",
        "docs": "/docs",
        "redoc": "/redoc",
        "version": "1.0.0",
        # Dependiendo de tu .env podrías estar en desarrollo o producción
        # Importa por que ayuda a validar comportamientos distintos
        # Es decir, en desarrollo podrías querer más logs o detalles de errores
        "environment": config.settings.ENVIRONMENT
    }


# Endpoint para verificar la salud de la API
@app.get("/health")
async def health_check():
    """ Endpoint para verificar que la API está funcionando correctamente """
    # Si no funcionara la API o si esta mal tu conexión a la DB
    # este endpoint debería reflejarlo
    return {
        "status": "healthy",
        "database_connected": ping_database()
    }
