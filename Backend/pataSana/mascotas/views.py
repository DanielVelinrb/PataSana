from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json, uuid, jwt, hashlib
from datetime import datetime, timedelta
from .utils import getUserID, mascotaExiste

@csrf_exempt
def registrar_mascota(request):

    if request.method == 'POST':
        data = json.loads(request.body)
        duenio = data.get('email')
        nombre = data.get('nombre')
        raza = data.get('raza')
        especie = data.get('especie')
        edad = data.get('edad')
        observaciones = data.get('observaciones')
        token = data.get('token')
        mascota_id = uuid.uuid4()

        duenio = getUserID(duenio)

        if(duenio is None):
            return JsonResponse({'error': 'DUEÑO INEXISTENTE.'}, status=400)

        duenio = duenio[0]

        try:
            payload = jwt.decode(token, 'pan', algorithms=['HS256'])
            user_rol = payload['user_rol']

            if(user_rol != "admin"):
                return JsonResponse({'error': 'USUARIO NO AUTORIZADO. SE REQUIEREN PERMISOS DE ADMINISTRADOR.'}, status=400)

            if(mascotaExiste(duenio, nombre) is not None):
                return JsonResponse({'error': 'EL USUARIO YA POSEE UNA MASCOTA CON ESTE NOMBRE.'}, status=400)

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO MASCOTA (ID, Nombre, Raza, Especie, Edad, Observaciones, id_dueno)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (mascota_id, nombre, raza, especie, edad, observaciones, duenio, )
                )
            
            return JsonResponse({'message': 'Mascota creada exitosamente'}, status=200)
        except jwt.ExpiredSignatureError:
            JsonResponse({'error': 'ERROR AL TRATAR DE REGISTRAR LA MASCOTA.'}, status=500)
        except jwt.DecodeError:
            JsonResponse({'error': 'ERROR AL TRATAR DE REGISTRAR LA MASCOTA.'}, status=500)     
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)



@csrf_exempt
def borrar_registro(request):

    if request.method == 'DELETE':
        data = json.loads(request.body)
        duenio = data.get('email')
        nombre = data.get('nombre')
        token = data.get('token')

        duenio = getUserID(duenio)

        if(duenio is None):
            return JsonResponse({'error': 'DUEÑO INEXISTENTE.'}, status=400)

        duenio = duenio[0]

        try:
            payload = jwt.decode(token, 'pan', algorithms=['HS256'])
            user_rol = payload['user_rol']

            if(user_rol != "admin"):
                return JsonResponse({'error': 'USUARIO NO AUTORIZADO. SE REQUIEREN PERMISOS DE ADMINISTRADOR.'}, status=400)

            if(mascotaExiste(duenio, nombre) is None):
                return JsonResponse({'error': 'EL USUARIO NO POSEE REGISTROS DE NINGUNA MASCOTA CON ESTE NOMBRE.'}, status=400)

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM MASCOTA where id_dueno = %s and nombre = %s
                    """,
                    (duenio, nombre)
                )
            
            return JsonResponse({'message': 'Registro eliminado exitosamente'}, status=200)
        except jwt.ExpiredSignatureError:
            JsonResponse({'error': 'ERROR AL TRATAR DE ELIMINAR EL REGISTRO DE LA MASCOTA.'}, status=500)
        except jwt.DecodeError:
            JsonResponse({'error': 'ERROR AL TRATAR DE ELIMINAR EL REGISTRO DE LA MASCOTA.'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)