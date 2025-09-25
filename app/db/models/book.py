from sqlmodel import SQLModel, Field


# Definición del modelo de datos para un libro
# Un modelo es una representación de una tabla en la base de datos
# Es un ORM (Object-Relational Mapping): Mapeo entre objetos y tablas
class Libro(SQLModel, table=True):
    """ Modelo de datos para un libro """
    # Básicamente es una tabla con columnas
    id: int | None = Field(default=None, primary_key=True)
    title: str  # Obligatorio
    author: str
    pages: int | None = None
    description: str | None = None  # "| None = None" indica que puede ser nulo
