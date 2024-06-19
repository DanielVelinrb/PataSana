from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
#from django.contrib.auth import authenticate
from django.db import connection
import json, uuid, jwt, hashlib
from .utils import existUser, validateUser
from datetime import datetime, timedelta

def home(request):
    return render(request, 'index.html')


@csrf_exempt
def crear_usuario(request):

    if request.method == 'POST':
        data = json.loads(request.body)
        nombre = data.get('nombre')
        email = data.get('email')
        password = data.get('password')
        rol = data.get('rol')

        user_exists = existUser(email)

        if user_exists is not None:
            return JsonResponse({'error': 'Correo inválido. El usuario ya existe'}, status=405)

        usuario_id = uuid.uuid4()
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO Usuario (ID, Nombre, Email, Password, Rol)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (usuario_id, nombre, email, password, "usuario",)
                )

            return JsonResponse({'message': 'Usuario creado exitosamente'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def iniciar_sesion(request):

    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        
        user = validateUser(email, password)

        if user is not None:
            token = jwt.encode({'user_id': user[0], 'user_rol': user[1]}, 'pan', algorithm='HS256')
            return JsonResponse({'token': token}, status=200)
            #return redirect('inicio')  # Cambia 'inicio' al nombre de tu vista de inicio
        else:
            return JsonResponse({'message': 'ERROR. CREDENCIALES INVÁLIDAS'}, status=400)
            #return redirect('login')  # Cambia 'login' al nombre de tu vista de login
    else:
        return JsonResponse({'message': 'ERROR. MÉTODO NO PERMITIDO'}, status=500)
        #return render(request, 'login.html')  # Cambia 'login.html' al nombre de tu template de login

@csrf_exempt
def cambiar_contrasenia(request):

    if request.method == 'PATCH':
        data = json.loads(request.body)
        password = data.get('password')
        email = data.get('email')

        user_exists = existUser(email)

        if user_exists is None:
            return JsonResponse({'error': 'ERROR. CORREO NO VÁLIDO'}, status=405)

        password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE Usuario SET password = %s where email = %s
                    """,
                    (password, email)
                )

            return JsonResponse({'message': 'CONTRASEÑA ACTUALIZADA CON ÉXITO'}, status=200)
        except Exception as e:
            return JsonResponse({'error': 'ERROR AL INTENTAR CAMBIAR LA CONTRASEÑA'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def obtener_usuarios(request):
    
    if request.method == 'GET':
        token = request.headers.get('Authorization')
        
        if not token:
            return JsonResponse({'error': 'ERROR. TOKEN DE IDENTIFICACION REQUERIDO'}, status=400)

        try:
            token = token.split(' ')[1]
            payload = jwt.decode(token, 'pan', algorithms=['HS256'])
            user_rol = payload['user_rol']

            if(user_rol != "admin"):
                return JsonResponse({'error': 'USUARIO NO AUTORIZADO. SE REQUIEREN PERMISOS DE ADMINISTRADOR.'}, status=400)

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

            return JsonResponse({'usuarios': usuarios}, status=200)
        except Exception as e:
            return JsonResponse({'error': 'ERROR AL OBTENER LOS USUARIOS'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def obtener_info_usuario(request):
    
    if request.method == 'GET':
        token = request.headers.get('Authorization')
        
        if not token:
            return JsonResponse({'error': 'ERROR. TOKEN DE IDENTIFICACION REQUERIDO'}, status=400)

        try:
            token = token.split(' ')[1]
            payload = jwt.decode(token, 'pan', algorithms=['HS256'])
            user_id = payload['user_id']

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM USUARIO where id = %s
                    """,
                    (user_id, )                    
                )

                usuario = cursor.fetchone()

                if usuario is None:
                    return JsonResponse({'error': "ERROR. EL USUARIO NO EXiSTE"}, status=200)

            return JsonResponse({'usuario': usuario}, status=200)
        except Exception as e:
            return JsonResponse({'error': 'ERROR AL OBTENER LA INFORMACION DEL USUARIO'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)



@csrf_exempt
def actualizar(request):

    if request.method == 'PATCH':
        data = json.loads(request.body)
        id_usuario = data.get('id')
        email = data.get('email')
        nombre = data.get('nombre')

        try:

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE Usuario SET email = %s, nombre = %s where id = %s
                    """,
                    (email, nombre, id_usuario, )
                )

            return JsonResponse({'message': 'DATOS DEL USUARIO ACTUALIZADOS CON EXITO'}, status=200)
        except Exception as e:
            return JsonResponse({'error': 'ERROR AL ACTUALIZAR LA INFORMACION'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
