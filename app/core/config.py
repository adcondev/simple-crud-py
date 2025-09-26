# Se empieza por el principio
import os

from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env.dev
# Solito hace el trabajo de leer el archivo y obtener las variables de entorno
# Si no existe .env.dev, no pasa nada, usará valores por defecto
# Ejemplo: DB_HOST: str = os.getenv("DB_HOST", "localhost") -> si no existe DB_HOST, usa "localhost"
load_dotenv("./.env.dev")


# Clase de configuración
# Lo que idealmente viene en .env.dev
# Como la base de datos es local, no hay problema en dejar las credenciales por defecto, si le meto una DB desde
# AWS/Azure/GCP entonces si me preocuparía por la seguridad
class Settings:
    # Configuración de base de datos
    DB_HOST: str = os.getenv("DB_HOST", "localhost")  #
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "postgres")
    DB_NAME: str = os.getenv("DB_NAME", "simple_crud_db")

    # URL de conexión completa
    # Una base de datos puede estar en local o en la nube, pero solo hace falta cambiar la URL
    DATABASE_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Configuración de la aplicación, puedes tener diversas configuraciones
    # para desarrollo, pruebas y producción
    # Por ejemplo, en producción podrías querer DEBUG=False, lo indicas en .env.dev.prod
    # Y en desarrollo DEBUG=True, lo indicas en .env.dev.dev
    # Así no tienes que cambiar el código, solo el archivo .env.dev que usas
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "dev")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"


# Aquí se hace accessible la configuración en toda la aplicación con solo un
# from app.core.config import settings
settings = Settings()
