# 🚀 Inicio Rápido - Simple CRUD API

## Ejecutar el proyecto (asumiendo PostgreSQL ya configurado)

### 1. Instalar dependencias
```bash
poetry install
```

### 2. Configurar PostgreSQL
```sql
-- En psql
CREATE DATABASE simple_crud_db;
```

### 3. Ajustar .env.dev si es necesario
```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=tu_password
DB_NAME=simple_crud_db
ENVIRONMENT=development
DEBUG=True
```

### 4. Ejecutar la API
```bash
poetry run uvicorn app.main:app --reload
```

### 5. Probar en el navegador
- API: http://localhost:8000
- Documentación: http://localhost:8000/docs
- Estado: http://localhost:8000/health

## Comandos útiles

### Probar conexión a DB
```bash
python -m app.db.session
```

### Crear un libro de prueba
```bash
curl -X POST "http://localhost:8000/books/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "1984",
    "author": "George Orwell",
    "pages": 328,
    "description": "Distopía clásica"
  }'
```

### Ver todos los libros
```bash
curl http://localhost:8000/books/
```

## Estructura del proyecto
```
app/
├── main.py              # Aplicación principal
├── api/endpoints/
│   └── books.py         # Endpoints CRUD
├── core/
│   └── config.py        # Configuración
└── db/
    ├── base.py          # Registro modelos
    ├── session.py       # Conexión DB
    └── models/
        └── libro.py     # Modelo libro
```

¡Listo para desarrollar! 🎉
