from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection
import json
import uuid

def getUserID(email):
    try:

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
