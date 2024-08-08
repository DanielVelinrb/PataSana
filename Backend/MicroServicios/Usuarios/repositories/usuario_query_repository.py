from database.dbConnection import postgresql_connection
from utils.mascotas_cliente import mascotas_por_usuario
from logger import get_logger
logger = get_logger(__name__)

def existUser(email):
    try:
        logger.info('Query existUser iniciada')
        connection = postgresql_connection()
        with connection.cursor() as cursor:

            cursor.execute(
                """
                Select * FROM usuario where email = %s
                """,
                (email,)
            )

            result = cursor.fetchone()
            logger.info('Query existUser finalizada')
            return result

    except Exception as e:
        logger.error(e)
        logger.error('ERROR existUser fallida')


def validateUser(email, password):
    try:
        logger.info('Query validateUser iniciada')
        connection = postgresql_connection()
        with connection.cursor() as cursor:

            cursor.execute(
                """
                Select ID, ROL FROM usuario where email = %s and password = %s
                """,
                (email, password, )
            )

            result = cursor.fetchone()
            logger.info('Query validateUser finalizada')
            return result

    except Exception as e:
        logger.error(e)
        logger.error('ERROR validateUser fallida')
        return


def obtener_usuarios_db(token):
    try:
        logger.info('Query obtener_usuarios_db iniciada')
        connection = postgresql_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT USUARIO.ID, USUARIO.NOMBRE, USUARIO.EMAIL 
                FROM USUARIO
                WHERE USUARIO.rol = 'usuario'
                """
            )
            usuarios = cursor.fetchall()
            mascotas_num = mascotas_por_usuario(token)
            usuarios_con_mascotas = []
            for usuario in usuarios:
                id_usuario = usuario[0]    
                usuarios_con_mascotas.append((usuario[0], usuario[1], usuario[2], 
                                                0 if id_usuario not in mascotas_num else mascotas_num[id_usuario]))
            
            logger.info('Query obtener_usuarios_db finalizada')
            return usuarios_con_mascotas

    except Exception as e:
        logger.error('ERROR obtener_usuarios_db fallida')
        logger.error(f"Error al obtener usuarios: {e}")
        return 500

def obtener_info_usuario_db(user_id):
    
    try:
        logger.info('Query obtener_info_usuario_db iniciada')
        connection = postgresql_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM USUARIO where id = %s
                """,
                (user_id, )                    
            )

            usuario = cursor.fetchone()
            logger.info('Query obtener_info_usuario_db finalizada')
            return usuario
    except Exception as e:
        logger.error('ERROR obtener_info_usuario_db fallida')