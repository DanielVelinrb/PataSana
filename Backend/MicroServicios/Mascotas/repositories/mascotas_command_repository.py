from database.dbConnection import postgresql_connection
from logger import get_logger
logger = get_logger(__name__)

def registrar_mascota_db(mascota_id, nombre, raza, especie, edad, observaciones, duenio):
    try:
        logger.info('Registro de mascotas iniciado')
        connection = postgresql_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO MASCOTA (ID, Nombre, Raza, Especie, Edad, Observaciones, id_dueno)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (mascota_id, nombre, raza, especie, edad, observaciones, duenio, )
            )
                
        connection.commit()
        connection.close()
        logger.info('Registro de mascotas finalizado')
        return 200
    except Exception as e:
        logger.error(e)
        return None

def borrar_registro_mascota(duenio, nombre):
    try:
        logger.info('Eliminacion registro de mascota iniciado')
        connection = postgresql_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM MASCOTA where id_dueno = %s and nombre = %s
                """,
                (duenio, nombre)
            )
            
        connection.commit()
        connection.close()
        logger.info('Eliminacion registro de mascota finalizado')
        return 200
    except Exception as e:
        logger.error(e)
        return None


def actualizar_registro_mascota(nombre, raza, especie, edad, observaciones, id_mascota):
    try:
        logger.info('Actualizacion registro mascota iniciado')
        connection = postgresql_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE MASCOTA SET 
                nombre = %s, raza = %s, especie = %s, edad = %s, observaciones = %s
                where id = %s
                """,
                (nombre, raza, especie, edad, observaciones, id_mascota, )
            )
            
        connection.commit()
        connection.close()
        logger.info('Actualizacion registro mascota finalizado')
        return 200
    except Exception as e:
        logger.error(e)
        return None