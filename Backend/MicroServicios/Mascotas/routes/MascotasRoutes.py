from flask import Blueprint, request, jsonify
from database.dbConnection import postgresql_connection
from utils.utils import getUserID, mascotaExiste
from repositories.mascotas_command_repository import registrar_mascota_db, borrar_registro_mascota, actualizar_registro_mascota
from repositories.mascotas_query_repository import obtener_total_mascotas, obtener_mascotas_usuario, obtener_info_mascota_db, mascotas_por_usuario
import hashlib, uuid, json, jwt

app = Blueprint('mascotas_blueprint', __name__)

@app.route('/registrar', methods=['POST'])
def registrar_mascota():
    data = request.json
    email = data.get('email')
    nombre = data.get('nombre')
    raza = data.get('raza')
    especie = data.get('especie')
    edad = data.get('edad')
    observaciones = data.get('observaciones')
    token = data.get('token')

    if token is None:
        return jsonify({'error': 'TOKEN FALTANTE.'}), 405

    duenio = getUserID(email)

    if(duenio is None):
        return jsonify({'error': 'DUEÑO INEXISTENTE.'}), 400

    try:
        payload = jwt.decode(token, 'pan', algorithms=['HS256'])
        user_rol = payload['user_rol']
        mascota_id = str(uuid.uuid4())
            
        if(user_rol != "admin"):
            return jsonify({'error': 'USUARIO NO AUTORIZADO. SE REQUIEREN PERMISOS DE ADMINISTRADOR.'}), 400

        if(mascotaExiste(duenio, nombre) is not None):
            return jsonify({'error': 'EL USUARIO YA POSEE UNA MASCOTA CON ESTE NOMBRE.'}), 400
            
        resultado = registrar_mascota_db(mascota_id, nombre, raza, especie, edad, observaciones, duenio)

        if(resultado is None):
            return jsonify({'error': 'ERROR AL TRATAR DE REGISTRAR LA MASCOTA.'}), 500
        return jsonify({'message': 'Mascota creada exitosamente'}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'ERROR AL TRATAR DE REGISTRAR LA MASCOTA.'}), 500
    except jwt.DecodeError:
        return jsonify({'error': 'ERROR AL TRATAR DE REGISTRAR LA MASCOTA.'}), 500   


@app.route('/borrar', methods=['DELETE'])
def borrar_registro():
    data = request.json
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
            return jsonify({'error': 'USUARIO NO AUTORIZADO. SE REQUIEREN PERMISOS DE ADMINISTRADOR.'}), 400

        if(mascotaExiste(duenio, nombre) is None):
            return jsonify({'error': 'EL USUARIO NO POSEE REGISTROS DE NINGUNA MASCOTA CON ESTE NOMBRE.'}), 400


        resultado = borrar_registro_mascota(duenio, nombre)

        if(resultado is None):
            return jsonify({'error': 'ERROR AL TRATAR DE REGISTRAR LA MASCOTA.'}), 500

        return jsonify({'message': 'Registro eliminado exitosamente'}), 200
    except jwt.ExpiredSignatureError:
        jsonify({'error': 'ERROR AL TRATAR DE ELIMINAR EL REGISTRO DE LA MASCOTA.'}), 500
    except jwt.DecodeError:
        jsonify({'error': 'ERROR AL TRATAR DE ELIMINAR EL REGISTRO DE LA MASCOTA.'}), 500


@app.route('/listar', methods=['GET'])
def obtener_mascotas():
    token = request.headers.get('Authorization')
        
    if not token:
        return jsonify({'error': 'ERROR. TOKEN DE IDENTIFICACION REQUERIDO'}), 400

    try:
        token = token.split(' ')[1]
        payload = jwt.decode(token, 'pan', algorithms=['HS256'])
        user_rol = payload['user_rol']
        user_id = payload['user_id']

        #if(user_rol != "usuario"):
        #   return JsonResponse({'error': 'ERROR. ESTE TIPO DE USUARIO NO PUEDE REALIZAR ESTA ACCION'}, status=400)
        mascotas = [] 
        if(user_rol == "usuario"):
            mascotas =  obtener_total_mascotas()

        if(user_rol == "admin"):
            mascotas = obtener_mascotas_usuario(user_id)

        if(mascotas == 500):
            return jsonify({'error': 'ERROR AL OBTENER LAS MASCOTAS'}), 500

        return jsonify({'mascotas': mascotas}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'ERROR AL OBTENER LAS MASCOTAS'}), 500


@app.route('/info', methods=['GET'])
def obtener_info_mascota():
    token = request.headers.get('Authorization')
    
    if not token:
        return jsonify({'error': 'ERROR. TOKEN DE IDENTIFICACION REQUERIDO'}), 400

    try:
        token = token.split(' ')[1]
        payload = jwt.decode(token, 'pan', algorithms=['HS256'])
        user_rol = payload['user_rol']
        user_id = payload['user_id']
        nombre = request.args.get('nombre', '')

        if nombre == '':
            return jsonify({'error': "FALTAN PARAMETROS EN LA CONSULTA"}), 200

        mascota = obtener_info_mascota_db(user_id, nombre)

        if mascota == 500:
            return jsonify({'error': "ERROR AL OBTENER EL REGISTRO"}), 200

        if mascota == 400:
            return jsonify({'error': "ERROR. EL USUARIO NO POSEE NINGUNA MASCOTA CON ESE NOMBRE"}), 200

        return jsonify({'mascota': mascota}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'ERROR AL OBTENER EL REGISTRO'}), 500


@app.route('/actualizar', methods=['PATCH'])
def actualizar():
    data = request.json
    id_mascota = data.get('id')
    nombre = data.get('nombre')
    raza = data.get('raza')
    especie = data.get('especie')
    edad = data.get('edad')
    observaciones = data.get('observaciones')

    if nombre is None or edad is None or especie is None or observaciones is None:
        return jsonify({'error': 'LOS CAMPOS A ACTUALIZAR NO PUEDEN SER NULOS'}), 405

    if not edad.isdigit() or (edad.isdigit() and int(edad) < 0):
        return jsonify({'error': 'LA EDAD INGRESADA DEBE SER UN NÚMERO ENTERO POSITIVO'}), 405
        
    try:

        resultado = actualizar_registro_mascota(nombre, raza, especie, edad, observaciones, id_mascota)

        if resultado is None:
            return jsonify({'message': 'ERROR AL ACTUALIZAR LA INFORMACION'}), 200

        return jsonify({'message': 'DATOS DE LA MASCOTA ACTUALIZADOS CON EXITO'}), 200
    except Exception as e:
        return jsonify({'error': 'ERROR AL ACTUALIZAR LA INFORMACION'}), 500



@app.route('/conteo', methods=['GET'])
def conteo_mascotas():
    token = request.headers.get('Authorization')
    
    if not token:
        return jsonify({'error': 'ERROR. TOKEN DE IDENTIFICACION REQUERIDO'}), 400

    try:
        token = token.split(' ')[1]
        payload = jwt.decode(token, 'pan', algorithms=['HS256'])
        user_rol = payload['user_rol']
        user_id = payload['user_id']

        conteo = mascotas_por_usuario()

        if conteo == 500:
            return jsonify({'error': "ERROR AL OBTENER EL CONTEO"}), 200

        return jsonify({'resultado': conteo}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'ERROR AL OBTENER EL CONTEO'}), 500