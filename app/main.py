# Gestor de contexto asíncrono(no te preocupes por eso por ahora)
from contextlib import asynccontextmanager

# Importa FastAPI para crear la aplicación web
from fastapi import FastAPI

# Importa configuración y funciones de la aplicación
from app.core import config
from app.db.session import create_tables, ping_database


# main.py debería ser simple, solo crear la app y definir los endpoints principales e importar routers(más endpoints)
# La lógica de negocio va en routers y servicios
# La lógica de datos va en db/models y db/session
# La configuración va en core/config.py

# lifespan es un gestor de contexto para el ciclo de vida de la aplicación
# Se usa para ejecutar código al iniciar y al finalizar la aplicación
@asynccontextmanager
async def lifespan(api: FastAPI):
    # Hacer antes del startup de la aplicación
    print(f"🚀 API({api}) iniciada en modo {config.settings.ENVIRONMENT}")
    create_tables()  # Crea las tablas si no existen
    # Correr la aplicación
    print("📚 API lista para recibir solicitudes")
    yield
    # Shutdown de la aplicación
    print("👋 Aplicación finalizada")


# Crear la instancia de FastAPI
# Aquí se configura la API con título, descripción, versión y URLs de documentación
# "/docs" -> Swagger UI
# "/redoc" -> ReDoc
# La documentación automática es una de las mejores características de FastAPI
# Ve a localhost:8000/docs o localhost:8000/redoc para verla.
# Ahí puedes probar los endpoints directamente desde el navegador, sin Postman ni curl, una chulada.
app = FastAPI(
    title="Simple CRUD FastAPI",
    description="Una API simple para aprender FastAPI con PostgreSQL",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan  # Muy importante ponerlo, sino no funciona el startup/shutdown
)


# app es la instancia principal de FastAPI
# async indica que la función es asíncrona, es decir,
# puede manejar múltiples solicitudes al mismo tiempo(Concurrencia es un tema avanzado, ntp)
# El decorador(@) indica el endpoint("/") y el métoodo HTTP(.get)
#
# Un decorador es un tipo de sandwich:
# def get(func, path):
#     """ Decorador para definir un endpoint GET """
#     def wrapper():
#         print("Hacer algo antes de la función")
#         root(path)
#         print("Hacer algo después de la función")
#     return wrapper
# Igual, ntp, de eso se encarga FastAPI
@app.get("/")  # Lo mismo que app.get(root, "/")
async def root():
    """ Endpoint raíz que proporciona información básica sobre la API """
    # Nada extraordinario, solo un mensaje de bienvenida
    return {
        "message": "Simple CRUD con FastAPI, SQLModel y PostgreSQL",
        "docs": "/docs",
        "redoc": "/redoc",
        "version": "1.0.0",
        # Dependiendo de tu .env.dev podrías estar en desarrollo o producción
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
