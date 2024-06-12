from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json, uuid, jwt, hashlib
from datetime import datetime, timedelta

@csrf_exempt
def registrar_mascota(request):

    if request.method == 'POST':
        data = json.loads(request.body)
        nombre = data.get('nombre')
        raza = data.get('raza')
        especie = data.get('especie')
        edad = data.get('edad')
        observaciones = data.get('observaciones')
        token = data.get('token')

        mascota_id = uuid.uuid4()

        try:
            payload = jwt.decode(token, 'pan', algorithms=['HS256'])
            duenio_id = payload['user_id']
            user_rol = payload['user_rol']
            print(duenio_id)
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO MASCOTA (ID, Nombre, Raza, Especie, Edad, Observaciones, id_dueno)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (mascota_id, nombre, raza, especie, edad, observaciones, duenio_id, )
                )
            
            return JsonResponse({'message': 'Mascota creada exitosamente'}, status=200)
        except jwt.ExpiredSignatureError:
            JsonResponse({'error': 'ERROR AL TRATAR DE REGISTRAR LA MASCOTA.'}, status=500)
        except jwt.DecodeError:
            JsonResponse({'error': 'ERROR AL TRATAR DE REGISTRAR LA MASCOTA.'}, status=500)     
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)