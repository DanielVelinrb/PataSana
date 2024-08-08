from database.dbConnection import postgresql_connection
from logger import get_logger
logger = get_logger(__name__)

def listar_visitas():
    try:
        logger.info('Consulta de visitas iniciada')
        connection = postgresql_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM Visitas
                """
            )
            visitas = cursor.fetchall()
        connection.commit()
        connection.close()
        logger.info('Consulta de visitas exitosa')
        return visitas
    except Exception as e:
        logger.error(e)
        return None