from database.dbConnection import postgresql_connection
from logger import get_logger
logger = get_logger(__name__)

def obtener_total_mascotas():
    try:
        logger.info('Obtencion mascotas inicializada')
        connection = postgresql_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM MASCOTA 
                """                
            )
            mascotas = cursor.fetchall()
        connection.commit()
        connection.close()
        logger.info('Mascotas obtenidas')
        return mascotas
    except Exception as e:
        return 500


def obtener_mascotas_usuario(user_id):
    try:
        logger.info('Obtencion mascotas de usuario iniciada')
        logger.info('USUARIO')
        logger.info(user_id)
        connection = postgresql_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM MASCOTA where id_dueno = %s
                """ ,
                (user_id, )                   
            )
            mascotas = cursor.fetchall()
        connection.commit()
        connection.close()
        logger.info('Obtencion mascotas de usuario finalizada')
        return mascotas
    except Exception as e:
        logger.error(e)
        return 500


def obtener_info_mascota_db(user_id, nombre):
    try:
        logger.info('Obtencion de mascota iniciada')
        connection = postgresql_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM MASCOTA where id_dueno = %s and nombre = %s
                """ ,
                (user_id, nombre, )               
            )
                    
            mascota = cursor.fetchone()
        connection.commit()
        connection.close()
        logger.info('Obtencion de mascota finalizada')
        if mascota is None:
            logger.info('No se encontro ningun registro')
            return 400
        return mascota
    except Exception as e:
        logger.error(e)
        return 500


def mascotas_por_usuario():
    try:
        logger.info('Conteo mascotas iniciado')
        connection = postgresql_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id_dueno, count(*) FROM MASCOTA 
                GROUP BY id_dueno
                """            
            )
                    
            conteo_mascotas = cursor.fetchall()
        connection.commit()
        connection.close()
        logger.info('Conteo finalizado')
        return {id_dueno: count for id_dueno, count in conteo_mascotas}
    except Exception as e:
        logger.error(e)
        return 500