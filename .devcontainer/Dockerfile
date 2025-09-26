# Un Dockerfile es un archivo de texto que contiene instrucciones para construir una imagen de Docker.

# FROM indica la imagen base que se utilizará
FROM python:3.13-slim

# ENV establece variables de entorno
# Evita que Python genere archivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Asegura que la salida de Python vaya directamente a la terminal
ENV PYTHONUNBUFFERED=1

# WORKDIR establece el directorio de trabajo dentro del contenedor
# Establece el directorio de trabajo
WORKDIR /app

# RUN ejecuta comandos en el contenedor durante la construcción
# Instalación mínima para desarrollo
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl git vim build-essential libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instala Poetry para la gestión de dependencias(FastAPI, SQLModel, y lo que estas necesiten(uvicorn))
# Instalar herramientas de desarrollo
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    pip install "fastapi[standard]" && \
    pip install pytest black isort

# Añade Poetry al PATH, es como agregar una variable de entorno en Windows
ENV PATH="/root/.local/bin:$PATH"


# COPY copia archivos desde el host al contenedor
# Primero copia los archivos de configuración de Poetry
# A lo que le vayas dando pip install, mientras estes en el ambiente virtual de Poetry,
# Poetry lo va a ir guardando en pyproject.toml y poetry.lock
COPY pyproject.toml poetry.lock* ./

# Para que Poetry no cree un entorno virtual dentro del contenedor,
# sino que instale las dependencias directamente en el entorno del contenedor
RUN poetry config virtualenvs.create false

# Poetry permite replicar el entorno de desarrollo fácilmente, te lo recomiendo mucho.
# --no-interaction evita que Poetry pida confirmaciones interactivas
# --no-ansi desactiva los códigos de color en la salida para que los logs sean más limpios
# Instala solo las dependencias (sin instalar el proyecto actual)
RUN poetry install --no-interaction --no-ansi --no-root

# Finalmente, copia el resto del código de la aplicación al contenedor
COPY . .

# Ahora instala el proyecto actual
RUN poetry install --no-interaction --no-ansi --only-root

# EXPOSE documenta qué puerto usa la aplicación
EXPOSE 8000

# CMD especifica el comando por defecto para ejecutar cuando se inicia el contenedor
# Mantener contenedor vivo sin ejecutar app
CMD ["sleep", "infinity"]


