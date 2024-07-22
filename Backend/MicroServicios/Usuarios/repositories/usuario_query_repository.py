from database.dbConnection import postgresql_connection


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


def obtener_usuarios_db():
    try:
        connection = postgresql_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT USUARIO.*, COUNT(MASCOTA.ID) AS mascotasNum 
                FROM USUARIO LEFT JOIN MASCOTA 
                ON USUARIO.ID = MASCOTA.id_dueno
                where USUARIO.rol = 'usuario'
                GROUP BY USUARIO.ID
                """                    
            )

            usuarios = cursor.fetchall()
            return usuarios
    except Exception as e:
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