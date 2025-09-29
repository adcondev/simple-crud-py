# Configuración centralizada de la aplicación
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env.dev
load_dotenv("./.env.dev")


class Settings:
    """Configuración de base de datos y entorno"""
    # Base de datos PostgreSQL
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "postgres")
    DB_NAME: str = os.getenv("DB_NAME", "simple_crud_db")

    # URL completa de conexión
    DATABASE_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Entorno de desarrollo
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "dev")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"


# Instancia global de configuración
settings = Settings()
