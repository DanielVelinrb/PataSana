from database.dbConnection import postgresql_connection
import json
import uuid

def getUserID(email):
    try:

        connection = postgresql_connection()
        with connection.cursor() as cursor:

            cursor.execute(
                """
                Select ID FROM Usuario where email = %s
                """,
                (email,)
            )

            result = cursor.fetchone()
            return result

    except Exception as e:
        print(e)


def mascotaExiste(id_duenio, nombre):
    try:

        connection = postgresql_connection()
        with connection.cursor() as cursor:

            cursor.execute(
                """
                Select * FROM MASCOTA where id_dueno = %s and nombre = %s
                """,
                (id_duenio, nombre,)
            )

            result = cursor.fetchone()
            return result

    except Exception as e:
        print(e)
