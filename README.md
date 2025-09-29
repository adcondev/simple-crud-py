# 📚 Simple CRUD API con FastAPI - Guía Paso a Paso

Esta guía te enseña a construir una **API REST completa** desde cero usando FastAPI y PostgreSQL. Ideal para desarrolladores junior que quieren aprender a crear APIs modernas con Python.

## 🎯 ¿Qué vamos a construir?

Una API para gestionar libros con todas las operaciones CRUD:
- ✅ **Crear** libros nuevos
- ✅ **Leer** libros (todos y por ID)  
- ✅ **Actualizar** libros existentes
- ✅ **Eliminar** libros
- ✅ **Buscar** libros por autor
- ✅ **Documentación automática** con Swagger

## 🛠️ Tecnologías utilizadas

- **FastAPI**: Framework moderno para APIs
- **SQLModel**: ORM para manejar la base de datos
- **PostgreSQL**: Base de datos relacional
- **Poetry**: Gestor de dependencias
- **Uvicorn**: Servidor ASGI para desarrollo

---

## 🚀 PASO 1: Configurar el entorno

### 1.1 Crear el directorio del proyecto
```bash
mkdir simple-crud-py
cd simple-crud-py
```

### 1.2 Inicializar Poetry (recomendado)
```bash
poetry init
# Seguir las instrucciones interactivas o usar los valores por defecto
```

### 1.3 Instalar dependencias
```bash
poetry add fastapi uvicorn[standard] sqlmodel psycopg2-binary python-dotenv
```

### 1.4 Crear la estructura de carpetas
```bash
mkdir -p app/api/endpoints app/core app/db/models
```

### 1.5 Crear archivos __init__.py
```bash
# En Windows
echo. > app/__init__.py
echo. > app/api/__init__.py  
echo. > app/api/endpoints/__init__.py
echo. > app/core/__init__.py
echo. > app/db/__init__.py
echo. > app/db/models/__init__.py

# En Linux/Mac
touch app/__init__.py app/api/__init__.py app/api/endpoints/__init__.py
touch app/core/__init__.py app/db/__init__.py app/db/models/__init__.py
```

---

## 🚀 PASO 2: Configurar la base de datos

### 2.1 Crear archivo de configuración (.env.dev)
```env
# Configuración PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=simple_crud_db

# Entorno
ENVIRONMENT=development
DEBUG=True
```

### 2.2 Crear configuración (app/core/config.py)
```python
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
```

---

## 🚀 PASO 3: Crear el modelo de datos

### 3.1 Modelo de libro (app/db/models/libro.py)
```python
from sqlmodel import SQLModel, Field

# Modelo de libro - Representa una tabla en PostgreSQL
class Libro(SQLModel, table=True):
    """Modelo principal para la gestión de libros"""
    id: int | None = Field(default=None, primary_key=True)
    title: str  # Título obligatorio
    author: str  # Autor obligatorio
    pages: int | None = None  # Páginas opcional
    description: str | None = None  # Descripción opcional

# Modelo para crear libros - Sin ID (se autogenera)
class LibroCrear(SQLModel):
    """Modelo para validar datos al crear/actualizar libros"""
    title: str
    author: str
    pages: int | None = None
    description: str | None = None
```

### 3.2 Registro de modelos (app/db/base.py)
```python
from sqlmodel import SQLModel

# Registro de modelos - Importar TODOS los modelos aquí
from app.db.models.libro import Libro

# Base SQLModel para crear tablas automáticamente
Base = SQLModel
```

---

## 🚀 PASO 4: Configurar la conexión a la base de datos

### 4.1 Sesión de base de datos (app/db/session.py)
```python
from sqlmodel import create_engine, Session, select
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
```

---

## 🚀 PASO 5: Crear los endpoints CRUD

### 5.1 Endpoints de libros (app/api/endpoints/books.py)
```python
# Endpoints CRUD para libros
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from app.db.models.libro import Libro, LibroCrear
from app.db.session import get_session

# Router con prefijo para agrupar endpoints
router = APIRouter(prefix="/books", tags=["books"])

# CREATE - Crear nuevo libro
@router.post("/", response_model=Libro, status_code=status.HTTP_201_CREATED)
async def crear_libro(libro: LibroCrear, session: Session = Depends(get_session)):
    """Crear un nuevo libro en la base de datos"""
    db_libro = Libro(**libro.model_dump())
    session.add(db_libro)
    session.commit()
    session.refresh(db_libro)  # Obtener ID generado
    return db_libro

# READ - Obtener todos los libros
@router.get("/", response_model=List[Libro])
async def obtener_libros(session: Session = Depends(get_session)):
    """Listar todos los libros disponibles"""
    statement = select(Libro)
    libros = session.exec(statement).all()
    return libros

# READ - Obtener libro por ID
@router.get("/{libro_id}", response_model=Libro)
async def obtener_libro(libro_id: int, session: Session = Depends(get_session)):
    """Obtener un libro específico por su ID"""
    libro = session.get(Libro, libro_id)
    if not libro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Libro con ID {libro_id} no encontrado"
        )
    return libro

# UPDATE - Actualizar libro existente
@router.put("/{libro_id}", response_model=Libro)
async def actualizar_libro(
    libro_id: int, 
    libro_actualizado: LibroCrear, 
    session: Session = Depends(get_session)
):
    """Actualizar datos de un libro existente"""
    libro = session.get(Libro, libro_id)
    if not libro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Libro con ID {libro_id} no encontrado"
        )
    
    # Actualizar solo campos proporcionados
    libro_data = libro_actualizado.model_dump(exclude_unset=True)
    for key, value in libro_data.items():
        setattr(libro, key, value)
    
    session.add(libro)
    session.commit()
    session.refresh(libro)
    return libro

# DELETE - Eliminar libro
@router.delete("/{libro_id}")
async def eliminar_libro(libro_id: int, session: Session = Depends(get_session)):
    """Eliminar un libro de la base de datos"""
    libro = session.get(Libro, libro_id)
    if not libro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Libro con ID {libro_id} no encontrado"
        )
    
    session.delete(libro)
    session.commit()
    return {"message": f"Libro '{libro.title}' eliminado correctamente"}

# SEARCH - Buscar por autor
@router.get("/buscar/por-autor", response_model=List[Libro])
async def buscar_libros_por_autor(
    autor: str, 
    session: Session = Depends(get_session)
):
    """Buscar libros por nombre del autor (búsqueda parcial)"""
    statement = select(Libro).where(Libro.author.ilike(f"%{autor}%"))
    libros = session.exec(statement).all()
    return libros
```

---

## 🚀 PASO 6: Crear la aplicación principal

### 6.1 Aplicación FastAPI (app/main.py)
```python
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
```

---

## 🚀 PASO 7: Configurar PostgreSQL

### 7.1 Instalar PostgreSQL
- **Windows**: Descargar desde [postgresql.org](https://www.postgresql.org/download/)
- **Mac**: `brew install postgresql`
- **Linux**: `sudo apt install postgresql postgresql-contrib`

### 7.2 Crear la base de datos
```sql
-- Conectar a PostgreSQL
psql -U postgres

-- Crear base de datos
CREATE DATABASE simple_crud_db;

-- Salir
\q
```

### 7.3 Verificar configuración
Edita el archivo `.env.dev` con tus credenciales de PostgreSQL.

---

## 🚀 PASO 8: Ejecutar la aplicación

### 8.1 Instalar dependencias finales
```bash
poetry install
```

### 8.2 Ejecutar servidor de desarrollo
```bash
# Con Poetry
poetry run uvicorn app.main:app --reload

# Sin Poetry
uvicorn app.main:app --reload
```

### 8.3 Verificar funcionamiento
- **API**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## ✅ ESTRUCTURA FINAL

```
simple-crud-py/
├── .env.dev                 # Variables de entorno
├── pyproject.toml          # Dependencias Poetry
└── app/
    ├── __init__.py
    ├── main.py             # Aplicación principal
    ├── api/
    │   ├── __init__.py
    │   └── endpoints/
    │       ├── __init__.py
    │       └── books.py    # Endpoints CRUD
    ├── core/
    │   ├── __init__.py
    │   └── config.py       # Configuración
    └── db/
        ├── __init__.py
        ├── base.py         # Registro de modelos
        ├── session.py      # Conexión DB
        └── models/
            ├── __init__.py
            └── libro.py    # Modelo de libro
```

---

## 🧪 PROBAR LA API

### Crear un libro
```bash
curl -X POST "http://localhost:8000/books/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "El Quijote",
    "author": "Miguel de Cervantes",
    "pages": 1000,
    "description": "Obra maestra de la literatura española"
  }'
```

### Obtener todos los libros
```bash
curl -X GET "http://localhost:8000/books/"
```

### Buscar por autor
```bash
curl -X GET "http://localhost:8000/books/buscar/por-autor?autor=Cervantes"
```

---

## 🎯 CONCEPTOS CLAVE APRENDIDOS

1. **Arquitectura limpia**: Separación de responsabilidades en capas
2. **ORM**: Mapeo objeto-relacional con SQLModel
3. **Dependencias**: Inyección de dependencias de FastAPI
4. **Validación**: Modelos Pydantic para validar datos
5. **Documentación**: Generación automática con OpenAPI
6. **Variables de entorno**: Configuración externalizada
7. **Ciclo de vida**: Manejo de startup/shutdown de la aplicación

---

## 🚀 PRÓXIMOS PASOS

### Funcionalidades que puedes agregar:
- **Autenticación JWT** para usuarios
- **Paginación** en listados
- **Filtros avanzados** (por género, año, etc.)
- **Validaciones personalizadas**
- **Tests unitarios** con pytest
- **Docker** para contenedores
- **Deploy** en la nube

### Nuevos modelos sugeridos:
- **Autor**: Información detallada de autores
- **Categoría**: Géneros literarios
- **Usuario**: Sistema de usuarios y favoritos
- **Préstamo**: Sistema de biblioteca

---

**¡Felicidades! 🎉 Has construido tu primera API REST completa con FastAPI.**

> Este esqueleto está diseñado para ser expandido. Úsalo como base para proyectos más complejos.
