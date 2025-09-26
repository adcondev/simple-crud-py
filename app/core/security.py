# Un poquito de Criptografía :)
from passlib.context import CryptContext

# Instancia global del contexto de encriptación
# bcrypt es un algoritmo de hash seguro y ampliamente utilizado
# "auto" maneja automáticamente la depreciación de esquemas antiguos
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Funciones para hashear y verificar contraseñas
# Hashear implica convertir la contraseña en texto plano a un formato seguro
#
# Imagina que dejas .env.dev en github, alguien obtiene la contraseña y URL, la usa para conectarse a la DB
# Esta persona vería las contraseñas en texto plano(tal y como están escritas)
# Si las contraseñas están hasheadas, no podría hacer nada con ellas
# Hash("MiContraseña123") -> "$2a$12$cDMZ/ex5b9mUBJGMiuU0.etnns.dJbz3SumMwml.I2opyGrLcbmyG"
#
# La cualidad de las funciones hash es que son unidireccionales:
# Computacionalmente es fácil convertir texto plano a hash,
# pero casi imposible revertirlo(el principio fundamental de la Criptografía)
def hash_password(password: str) -> str:
    """ Hashea una contraseña en texto plano """
    return pwd_context.hash(password)


# Verifica si una contraseña en texto plano coincide con su hash
# Idealmente, hay una correspondencia uno a uno entre el hash y la contraseña
# ("idealmente", por que puede haber "colisiones", pero eso es mas avanzado)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ Verifica si una contraseña en texto plano coincide con su hash """
    return pwd_context.verify(plain_password, hashed_password)
