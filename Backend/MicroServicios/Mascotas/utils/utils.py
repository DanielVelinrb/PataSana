from database.dbConnection import postgresql_connection
import json
import uuid, requests


def getUserID(email):
    try:
        url = 'http://172.20.0.2:8081/usuarios/exist'
        params = {'email': email}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            mascotas = response.json()
            return mascotas.get('id')

        return None
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
