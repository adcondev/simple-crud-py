from sqlmodel import SQLModel
# Es importante importar todos los modelos aquí
# para que SQLModel pueda registrarlos y crear las tablas

# Base es la clase base para todos los modelos
Base = SQLModel

# Un Modelo es la representación de una tabla en la base de datos
# o la estructura de un JSON en una solicitud/respuesta HTTP
# SQLModel permite usar los modelos tanto para la base de datos como para las solicitudes HTTP
