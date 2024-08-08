from database.dbConnection import postgresql_connection
import hashlib, uuid
from logger import get_logger
logger = get_logger(__name__)

def crear_usuario(nombre, email, password):
    try:
        logger.info('Query crear_usuario iniciada')
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        connection = postgresql_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO Usuario (ID, Nombre, Email, Password, Rol)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (str(uuid.uuid4()), nombre, email, password, "usuario",)
            )
        connection.commit()
        connection.close()
        logger.info('Query crear_usuario finalizada con exito')
        return 200
    except Exception as e:
        logger.error(e)
        logger.error('ERROR crear_usuario fallida')
        return None


def cambiar_contrasenia_db(password, email):
    try:
        logger.info('Query cambiar_contrasenia_db iniciada')
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        connection = postgresql_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE Usuario SET password = %s where email = %s
                """,
                (password, email)
            )
        connection.commit()
        connection.close()
        logger.info('Query cambiar_contrasenia_db finalizada con exito')
        return 200
    except Exception as e:
        logger.error(e)
        logger.error('ERROR cambiar_contrasenia_db fallida')
        return None


def actualizar_db(id_usuario, nombre, email):
    try:
        logger.info('Query actualizar_db iniciada')
        connection = postgresql_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE Usuario SET email = %s, nombre = %s where id = %s
                """,
                (email, nombre, id_usuario, )
            )
        connection.commit()
        connection.close()
        logger.info('Query actualizar_db finalizada')
        return 200
    except Exception as e:
        logger.error(e)
        logger.error('ERROR actualizar_db fallida')
