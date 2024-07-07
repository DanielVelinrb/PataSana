from database.dbConnection import postgresql_connection
import json
import uuid
import re

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
        print(e)

def correoValido(email):
    regex = r'^[a-zA-Z0-9][a-zA-Z0-9._]{3,}[a-zA-Z0-9]@(hotmail\.com|gmail\.com|outlook\.com|epn\.edu\.ec)$'

    if re.match(regex, email):
        return True
    else:
        return False
