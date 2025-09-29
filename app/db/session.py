from sqlmodel import create_engine, Session, select  # Object Relational Mapper (ORM) para bases de datos SQL

from app.core.config import settings
from app.db.base import Base

# Motor de base de datos con configuración optimizada
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Mostrar SQL en modo debug
    pool_pre_ping=True,   # Verificar conexiones
    pool_recycle=300      # Reciclar cada 5 min
)


def create_tables():
    """Crear todas las tablas automáticamente"""
    print(f"🔗 Conectando a: {settings.DB_HOST}")
    try:
        Base.metadata.create_all(engine)
        print("✅ Tablas creadas exitosamente")
    except Exception as e:
        print(f"❌ Error creando tablas: {e}")


def get_session():
    """Dependencia para obtener sesión de DB"""
    with Session(engine) as session:
        yield session


def ping_database():
    """Verificar conexión a PostgreSQL"""
    try:
        with Session(engine) as session:
            session.exec(select(1))
        return True
    except Exception as e:
        print(f"❌ DB desconectada: {e}")
        return False


# Prueba de conexión si se ejecuta directamente
if __name__ == "__main__":
    print("🔍 Probando conexión...")
    if ping_database():
        print("✅ Conexión exitosa")
    else:
        print("❌ Fallo de conexión")
