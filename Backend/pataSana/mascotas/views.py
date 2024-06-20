from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json, uuid, jwt, hashlib
from datetime import datetime, timedelta
from .utils import getUserID, mascotaExiste


#def home(request):
#    return render(request, 'mascotas/lista_mascotas.html')

@csrf_exempt
def registrar_mascota(request):

    if request.method == 'POST':
        data = json.loads(request.body)
        duenio = data.get('email')
        nombre = data.get('nombre')
        raza = data.get('raza')
        especie = data.get('especie')
        edad = str(data.get('edad'))
        observaciones = data.get('observaciones')
        token = data.get('token')
        mascota_id = uuid.uuid4()

        duenio = getUserID(duenio)

        if(duenio is None):
            return JsonResponse({'error': 'DUEÑO INEXISTENTE.'}, status=400)

        #duenio = duenio[0]

        try:
            payload = jwt.decode(token, 'pan', algorithms=['HS256'])
            user_rol = payload['user_rol']

            #if(user_rol != "admin"):
            #    return JsonResponse({'error': 'USUARIO NO AUTORIZADO. SE REQUIEREN PERMISOS DE ADMINISTRADOR.'}, status=400)

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


@csrf_exempt
def obtener_mascotas(request):
    
    if request.method == 'GET':
        token = request.headers.get('Authorization')
        
        if not token:
            return JsonResponse({'error': 'ERROR. TOKEN DE IDENTIFICACION REQUERIDO'}, status=400)

        try:
            token = token.split(' ')[1]
            payload = jwt.decode(token, 'pan', algorithms=['HS256'])
            user_rol = payload['user_rol']
            user_id = payload['user_id']

            #if(user_rol != "usuario"):
            #   return JsonResponse({'error': 'ERROR. ESTE TIPO DE USUARIO NO PUEDE REALIZAR ESTA ACCION'}, status=400)

            with connection.cursor() as cursor:
                if(user_rol == "usuario"):
                    cursor.execute(
                        """
                        SELECT * FROM MASCOTA where id_dueno = %s
                        """ ,
                        (user_id, )               
                    )
                if(user_rol == "admin"):
                    cursor.execute(
                        """
                        SELECT * FROM MASCOTA 
                        """                
                    )
                mascotas = cursor.fetchall()

            return JsonResponse({'mascotas': mascotas}, status=200)
        except Exception as e:
            return JsonResponse({'error': 'ERROR AL OBTENER LAS MASCOTAS'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)



@csrf_exempt
def obtener_info_mascota(request):
    
    if request.method == 'GET':
        token = request.headers.get('Authorization')
        
        if not token:
            return JsonResponse({'error': 'ERROR. TOKEN DE IDENTIFICACION REQUERIDO'}, status=400)

        try:
            token = token.split(' ')[1]
            payload = jwt.decode(token, 'pan', algorithms=['HS256'])
            user_rol = payload['user_rol']
            user_id = payload['user_id']
            nombre = request.GET.get('nombre', '')

            if nombre == '':
                return JsonResponse({'error': "FALTAN PARAMETROS EN LA CONSULTA"}, status=200)

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM MASCOTA where id_dueno = %s and nombre = %s
                    """ ,
                    (user_id, nombre, )               
                )
                
                mascota = cursor.fetchone()

                if mascota is None:
                    return JsonResponse({'error': "ERROR. EL USUARIO NO POSEE NINGUNA MASCOTA CON ESE NOMBRE"}, status=200)

            return JsonResponse({'mascota': mascota}, status=200)
        except Exception as e:
            return JsonResponse({'error': 'ERROR AL OBTENER LAS MASCOTAS'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def actualizar(request):
    
    if request.method == 'PATCH':
        data = json.loads(request.body)
        id_mascota = data.get('id')
        nombre = data.get('nombre')
        raza = data.get('raza')
        especie = data.get('especie')
        edad = data.get('edad')
        observaciones = data.get('observaciones')

        if nombre is None or edad is None or especie is None or observaciones is None:
            return JsonResponse({'error': 'LOS CAMPOS A ACTUALIZAR NO PUEDEN SER NULOS'}, status=405)

        print("pollo")

        if not edad.isdigit() or (edad.isdigit() and int(edad) < 0):
            return JsonResponse({'error': 'LA EDAD INGRESADA DEBE SER UN NÚMERO ENTERO POSITIVO'}, status=405)
        
        print("pan")

        try:

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE MASCOTA SET 
                    nombre = %s, raza = %s, especie = %s, edad = %s, observaciones = %s
                    where id = %s
                    """,
                    (nombre, raza, especie, edad, observaciones, id_mascota, )
                )
            print("pato")
            return JsonResponse({'message': 'DATOS DE LA MASCOTA ACTUALIZADOS CON EXITO'}, status=200)
        except Exception as e:
            return JsonResponse({'error': 'ERROR AL ACTUALIZAR LA INFORMACION'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)