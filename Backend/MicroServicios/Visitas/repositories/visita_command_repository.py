from database.dbConnection import postgresql_connection
import hashlib, uuid
from logger import get_logger
logger = get_logger(__name__)

def registrar_visita(fecha, duenio, observaciones, nombre_mascota):
    try:
        logger.info('Query de registro de visitas iniciada')
        connection = postgresql_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO Visitas (Id, Fecha, Duenio, Observaciones, Nombremascota)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (str(uuid.uuid4()), fecha, duenio, observaciones, nombre_mascota,)
            )
        connection.commit()
        connection.close()
        logger.info('Query de registro de visitas finalizada')
        return 200
    except Exception as e:
        logger.error(e)
        return None