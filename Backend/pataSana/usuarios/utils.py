from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json
import uuid
import re

def existUser(email):
    try:
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

    print(re.match(regex, email))
    if re.match(regex, email):
        return True
    else:
        return False
