from flask import Blueprint, request, jsonify
from database.dbConnection import postgresql_connection
import hashlib, uuid, json, jwt
from utils.utils import existUser, validateUser, correoValido
import uuid

app = Blueprint('users_blueprint', __name__)


@app.route('/crear', methods=['POST'])
def crearUsuario():
    data = request.json 
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')
    
    #VALIDA QUE NINGUNO DE LOS CAMPOS SOLICITADOS SEA NULO
    if(nombre is None or email is None or password is None):
        jsonify({'mensaje': 'CUERPO DE LA SOLICITUD INCORRECTO.'}), 400

    #VALIDAR DOMINIO DE LOS CAMPOS

    #VALIDA QUE NO EXISTA UN USUARIO CON ESE CORREO
    if existUser(email):
        return jsonify({'mensaje': 'ERROR. YA EXISTE UN USUARIO CON ESTE CORREO'}), 400

    usuario_id = str(uuid.uuid4())

    if(len(password) <= 3):
        return jsonify({'error': 'Contraseña debil. La contraseña debe poseer al menos 4 caracteres.'}), 405

    password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    try:
        connection = postgresql_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO Usuario (ID, Nombre, Email, Password, Rol)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (usuario_id, nombre, email, password, "usuario",)
            )
        connection.commit()
        connection.close()

        return jsonify({'message': 'Usuario creado exitosamente'}), 200
    except Exception as e:
         return jsonify({'error': str(e)}), 500
    

@app.route('/login', methods=['POST'])
def login():
    data = request.json 
    email = data.get('email')
    password = data.get('password')
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    user = validateUser(email, password)

    if user is not None:
        token = jwt.encode({'user_id': user[0], 'user_rol': user[1]}, 'pan', algorithm='HS256')
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'ERROR. CREDENCIALES INVÁLIDAS'}), 400


@app.route('/change_password', methods=['PATCH'])
def cambiar_contrasenia():
    data = request.json
    password = data.get('password')
    email = data.get('email')

    user_exists = existUser(email)

    if user_exists is None:
        return jsonify({'error': 'ERROR. CORREO NO VÁLIDO'}), 405

    if(len(password) <= 3):
        return jsonify({'error': 'Contraseña debil. La contraseña debe poseer al menos 4 caractéres.'}), 405

    password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    try:
        connection = postgresql_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE Usuario SET password = %s where email = %s
                """,
                (password, email)
            )
        connection.commit()
        connection.close()

        return jsonify({'message': 'CONTRASEÑA ACTUALIZADA CON ÉXITO'}), 200
    except Exception as e:
        return jsonify({'error': 'ERROR AL INTENTAR CAMBIAR LA CONTRASEÑA'}), 500
    

@app.route('/get_users', methods=['GET'])
def obtener_usuarios():
    token = request.headers.get('Authorization')
        
    if not token:
        return jsonify({'error': 'ERROR. TOKEN DE IDENTIFICACION REQUERIDO'}), 400

    try:
        token = token.split(' ')[1]
        payload = jwt.decode(token, 'pan', algorithms=['HS256'])
        user_rol = payload['user_rol']

        if(user_rol != "admin"):
            return jsonify({'error': 'USUARIO NO AUTORIZADO. SE REQUIEREN PERMISOS DE ADMINISTRADOR.'}), 400

        connection = postgresql_connection()
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

        return jsonify({'usuarios': usuarios}), 200
    except Exception as e:
        return jsonify({'error': 'ERROR AL OBTENER LOS USUARIOS'}), 500


@app.route('/get_info_user', methods=['GET'])
def obtener_info_usuario():
    token = request.headers.get('Authorization')
        
    if not token:
        return jsonify({'error': 'ERROR. TOKEN DE IDENTIFICACION REQUERIDO'}), 400

    try:
        token = token.split(' ')[1]
        payload = jwt.decode(token, 'pan', algorithms=['HS256'])
        user_id = payload['user_id']

        connection = postgresql_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM USUARIO where id = %s
                """,
                (user_id, )                    
            )

            usuario = cursor.fetchone()

            if usuario is None:
                return jsonify({'error': "ERROR. EL USUARIO NO EXiSTE"}), 404

        return jsonify({'usuario': usuario}), 200
    except Exception as e:
        return jsonify({'error': 'ERROR AL OBTENER LA INFORMACION DEL USUARIO'}), 500


@app.route('/actualizar_datos', methods=['PATCH'])
def actualizar():
    data = request.json
    id_usuario = data.get('id')
    email = data.get('email')
    nombre = data.get('nombre')

    if correoValido(email) is False:
        return jsonify({'error': 'Correo inválido. Este correo no cumple con el formato adecuado.'}), 405

    if nombre is None:
        return jsonify({'error': 'ERROR. No se puede actualizar un nombre a un valor en blanco.'}), 405

    try:
        connection = postgresql_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE Usuario SET email = %s, nombre = %s where id = %s
                """,
                (email, nombre, id_usuario, )
            )
        connection.commit()
        connection.close()

        return jsonify({'message': 'DATOS DEL USUARIO ACTUALIZADOS CON EXITO'}), 200
    except Exception as e:
        return jsonify({'error': 'ERROR AL ACTUALIZAR LA INFORMACION'}), 500
