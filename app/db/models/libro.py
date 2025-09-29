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
