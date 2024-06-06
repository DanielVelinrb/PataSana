from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json

def home(request):
    return HttpResponse("¡Hola, mundo!")


import uuid

@csrf_exempt
def crear_usuario(request):
    if request.method == 'POST':
        print(request)
        # Obtener datos del cuerpo de la solicitud
        data = json.loads(request.body)
        nombre = data.get('nombre')
        email = data.get('email')
        password = data.get('password')
        rol = data.get('rol')

        print(nombre)

        # Generar un UUID único para el ID del usuario
        usuario_id = uuid.uuid4()

        # Intentar insertar el usuario en la base de datos
        try:
            with connection.cursor() as cursor:
                # Ejecutar la consulta SQL para insertar el usuario
                cursor.execute(
                    """
                    INSERT INTO Usuario (ID, Nombre, Email, Password, Rol)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (2, nombre, email, password, rol)
                )

            return JsonResponse({'message': 'Usuario creado exitosamente'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)