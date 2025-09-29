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
