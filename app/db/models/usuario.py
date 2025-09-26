from sqlmodel import SQLModel, Field


# Definición del modelo de datos para un usuario
class Usuario(SQLModel, table=True):
    """ Modelo de datos para un usuario """
    id: int | None = Field(default=None, primary_key=True)
    username: str
    email: str
    hashed_password: str


# Modelo para crear un usuario (sin id, que es autogenerado)
class UsuarioCrear(SQLModel):
    username: str
    email: str
    password: str  # Contraseña, se debe hashear antes de guardar
