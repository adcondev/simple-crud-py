from sqlmodel import SQLModel

# Registro de modelos - Importar TODOS los modelos aquí
from app.db.models.libro import Libro

# Base SQLModel para crear tablas automáticamente
Base = SQLModel
