from sqlmodel import create_engine, Session, select

# Notaras que hay varios archivos __init__.py
# Esto es para que Python trate los directorios como paquetes
# y puedas importar módulos desde ellos
from app.core.config import settings
# Base contiene la metadata de los modelos, apartir de la cual se crean las tablas
from app.db.base import Base

# Crear el motor de base de datos usando la configuración
# engine representa la conexión a la base de datos
engine = create_engine(
    # La URL de settings que viene del archivo .env.dev :)
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Mostrar SQL queries en modo debug
    pool_pre_ping=True,  # Verificar conexiones antes de usarlas
    pool_recycle=300  # Reciclar conexiones cada 5 minutos
)


# Tener 2 tablas es nada, pero si tienes 20 o 50 tablas?
# No quieres andar creando tablas una por una manualmente en PostgreSQL(pgAdmin, Datagrip)
def create_tables():
    """ Crear las tablas en la base de datos """
    print(f"🔗 Conectado a DB: {settings.DB_HOST}")
    try:
        # con los modelos de Base crea las tablas en la base de datos
        Base.metadata.create_all(engine)
        print("✅ Tablas creadas correctamente")
    except Exception as e:
        print(f"❌ Error al crear tablas: {e}")


# Dependencia para obtener una sesión de base de datos
def get_session():
    """ Obtener una sesión de base de datos """
    with Session(engine) as session:
        yield session


# Un ping es un chequeo rápido para ver si la base de datos responde
# try/except/finally para manejar errores de conexión, si algo sale mal en try, va a except, y el programa no se cae
# finally siempre se ejecuta al final, ya sea que haya error en try o no
def ping_database():
    """ Verificar la conexión a la base de datos """
    try:
        with Session(engine) as session:
            statement = select(1)
            session.exec(statement)
            # Retorna un 1 desde PostgreSQL, se ejecuta en la db asi que verifica la conexión
        return True
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return False
    finally:
        print("Intento de conexión a la base de datos finalizado")


# Revisar la conexión a la base de datos al iniciar el script
# Esta validación indica que solo se ejecuta desde línea de comandos
# python app/db/session.py
# No se ejecuta si se importa este módulo
# import app.db.session
if __name__ == "__main__":
    print("Probando la conexión a la base de datos...")
    if ping_database():
        print("✅ Conexión exitosa a la base de datos")
    else:
        print("❌ No se pudo conectar a la base de datos")
