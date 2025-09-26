from sqlmodel import create_engine, Session, select

from app.core.config import settings
from app.db.base import Base

# Crear el motor de base de datos usando la configuración
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Mostrar SQL queries en modo debug
    pool_pre_ping=True,  # Verificar conexiones antes de usarlas
    pool_recycle=300  # Reciclar conexiones cada 5 minutos
)


def create_tables():
    """ Crear las tablas en la base de datos """
    try:
        Base.metadata.create_all(engine)
        print("✅ Tablas creadas correctamente")
    except Exception as e:
        print(f"❌ Error al crear tablas: {e}")


def get_session():
    """ Obtener una sesión de base de datos """
    with Session(engine) as session:
        yield session


def ping_database():
    """ Verificar la conexión a la base de datos """
    try:
        with Session(engine) as session:
            # Retorna un 1, se ejecuta en la db asi que verifica la conexión
            statement = select(1)
            session.exec(statement)
        return True
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return False
