from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json, uuid, jwt, hashlib
from datetime import datetime, timedelta

@csrf_exempt
def registrar_producto(request):

    if request.method == 'POST':
        data = json.loads(request.body)
        nombre = data.get('nombre')
        precio = data.get('precio')
        descripcion = data.get('descripcion')
        cantidad = data.get('cantidad')
        token = data.get('token')

        producto_id = uuid.uuid4()

        try:
            payload = jwt.decode(token, 'pan', algorithms=['HS256'])
            user_rol = payload['user_rol']
            
            if(user_rol != 'admin'):
                return JsonResponse({'message': 'Permisos Denegados'}, status=500)

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO PRODUCTO (ID, Nombre, Precio, Descripcion, Cantidad)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (producto_id, nombre, precio, descripcion, cantidad, )
                )
            
            return JsonResponse({'message': 'Producto creado exitosamente'}, status=200)
        except jwt.ExpiredSignatureError:
            JsonResponse({'error': 'ERROR AL TRATAR DE CREAR EL PRODUCTO.'}, status=500)
        except jwt.DecodeError:
            JsonResponse({'error': 'ERROR AL TRATAR DE REGISTRAR LA MASCOTA.'}, status=500)     
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)