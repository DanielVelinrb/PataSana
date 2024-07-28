from database.dbConnection import postgresql_connection
from utils.mascotas_cliente import mascotas_por_usuario


def existUser(email):
    try:
        connection = postgresql_connection()
        with connection.cursor() as cursor:

            cursor.execute(
                """
                Select * FROM usuario where email = %s
                """,
                (email,)
            )

            result = cursor.fetchone()
            return result

    except Exception as e:
        print(e)


def validateUser(email, password):
    try:
        connection = postgresql_connection()
        with connection.cursor() as cursor:

            cursor.execute(
                """
                Select ID, ROL FROM usuario where email = %s and password = %s
                """,
                (email, password, )
            )

            result = cursor.fetchone()
            return result

    except Exception as e:
        return


def obtener_usuarios_db(token):
    try:
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

            return usuarios_con_mascotas

    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return 500

def obtener_info_usuario_db(user_id):
    
    try:
        connection = postgresql_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM USUARIO where id = %s
                """,
                (user_id, )                    
            )

            usuario = cursor.fetchone()
            return usuario
    except Exception as e:
        print(e)