from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
#from django.contrib.auth import authenticate
from django.db import connection
import json, uuid, jwt, hashlib
from .utils import existUser, validateUser
from datetime import datetime, timedelta

def home(request):
    return HttpResponse("¡Hola, mundo!")

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
                    (usuario_id, nombre, email, password, rol,)
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
    print(request.method)
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