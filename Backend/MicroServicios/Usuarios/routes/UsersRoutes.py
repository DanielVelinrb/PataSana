from flask import Blueprint, request, jsonify
import hashlib, json, jwt
from utils.utils import correoValido
from repositories.usuario_query_repository import existUser, validateUser, obtener_usuarios_db, obtener_info_usuario_db
from repositories.usuario_command_repository import crear_usuario, cambiar_contrasenia_db, actualizar_db
from logger import get_logger
logger = get_logger(__name__)


app = Blueprint('users_blueprint', __name__)


@app.route('/crear', methods=['POST'])
def crearUsuario():
    logger.info('Creacion usuario iniciada')
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

    if(len(password) <= 3):
        return jsonify({'error': 'Contraseña debil. La contraseña debe poseer al menos 4 caracteres.'}), 405

    try:
        resultado = crear_usuario(nombre, email, password)

        if(resultado is None):
            return jsonify({'ERROR': 'ERROR AL CREAR EL USUARIO'}), 500

        logger.info('Creacion usuario exitosa')
        return jsonify({'message': 'Usuario creado exitosamente'}), 200
    except Exception as e:
         logger.error(str(e))
         return jsonify({'error': str(e)}), 500
    

@app.route('/login', methods=['POST'])
def login():
    logger.info('LogIn iniciado')
    data = request.json 
    email = data.get('email')
    password = data.get('password')
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    user = validateUser(email, password)

    if user is not None:
        token = jwt.encode({'user_id': user[0], 'user_rol': user[1]}, 'pan', algorithm='HS256')
        logger.info('LogIn exitoso')
        return jsonify({'token': token}), 200
    else:
        logger.error(f'ERROR. CREDENCIALES INVÁLIDAS {email} {password}')
        return jsonify({'message': 'ERROR. CREDENCIALES INVÁLIDAS'}), 400


@app.route('/change_password', methods=['PATCH'])
def cambiar_contrasenia():
    logger.info('Cambio contraseña iniciada')
    data = request.json
    password = data.get('password')
    email = data.get('email')

    user_exists = existUser(email)

    if user_exists is None:
        return jsonify({'error': 'ERROR. CORREO NO VÁLIDO'}), 405

    if(len(password) <= 3):
        return jsonify({'error': 'Contraseña debil. La contraseña debe poseer al menos 4 caractéres.'}), 405

    try:
        resultado = cambiar_contrasenia_db(password, email)
        if(resultado is None):
            return jsonify({'ERROR': 'ERROR AL ACTUALIZAR LA CONTRASEÑA'}), 500

        logger.info('Cambio contraseña exitoso')
        return jsonify({'message': 'CONTRASEÑA ACTUALIZADA CON ÉXITO'}), 200
    except Exception as e:
        logger.error(e)
        return jsonify({'error': 'ERROR AL INTENTAR CAMBIAR LA CONTRASEÑA'}), 500
    

@app.route('/get_users', methods=['GET'])
def obtener_usuarios():
    logger.info('Obtener usuarios iniciado')
    token = request.headers.get('Authorization')
        
    if not token:
        return jsonify({'error': 'ERROR. TOKEN DE IDENTIFICACION REQUERIDO'}), 400

    try:
        token = token.split(' ')[1]
        payload = jwt.decode(token, 'pan', algorithms=['HS256'])
        user_rol = payload['user_rol']

        if(user_rol != "admin"):
            return jsonify({'error': 'USUARIO NO AUTORIZADO. SE REQUIEREN PERMISOS DE ADMINISTRADOR.'}), 400

        resultado = obtener_usuarios_db(token)
        if(resultado == 500):
            return jsonify({'ERROR': 'ERROR AL OBTENER LOS USUARIOS'}), 500

        logger.info('Usuarios obtenidos exitosamente')
        return jsonify({'usuarios': resultado}), 200
    except Exception as e:
        logger.error('ERROR AL OBTENER LOS USUARIOS')
        logger.error(e)
        return jsonify({'error': 'ERROR AL OBTENER LOS USUARIOS'}), 500


@app.route('/get_info_user', methods=['GET'])
def obtener_info_usuario():
    logger.info('Obtener info usario')
    token = request.headers.get('Authorization')
        
    if not token:
        return jsonify({'error': 'ERROR. TOKEN DE IDENTIFICACION REQUERIDO'}), 400

    try:
        token = token.split(' ')[1]
        payload = jwt.decode(token, 'pan', algorithms=['HS256'])
        user_id = payload['user_id']

        usuario = obtener_info_usuario_db(user_id)
        logger.info('USUARIO')
        logger.info(usuario)
        if usuario is None:
            return jsonify({'error': "ERROR. EL USUARIO NO EXiSTE"}), 404

        logger.info('Obtener info usario exitoso')
        return jsonify({'usuario': usuario}), 200
    except Exception as e:
        logger.error('ERROR AL OBTENER LA INFORMACION DEL USUARIO')
        return jsonify({'error': 'ERROR AL OBTENER LA INFORMACION DEL USUARIO'}), 500


@app.route('/actualizar_datos', methods=['PATCH'])
def actualizar():
    logger.info('Actualizacion de datos del usuario iniciada')
    data = request.json
    id_usuario = data.get('id')
    email = data.get('email')
    nombre = data.get('nombre')

    if correoValido(email) is False:
        return jsonify({'error': 'Correo inválido. Este correo no cumple con el formato adecuado.'}), 405

    if nombre is None:
        return jsonify({'error': 'ERROR. No se puede actualizar un nombre a un valor en blanco.'}), 405

    try:
        resultado = actualizar_db(id_usuario, nombre, email)

        if(resultado is None):
            return jsonify({'ERROR': 'ERROR AL ACTUALIZAR LOS DATOS DEL USUARIO'}), 500

        logger.info('DATOS DEL USUARIO ACTUALIZADOS CON EXITO')
        return jsonify({'message': 'DATOS DEL USUARIO ACTUALIZADOS CON EXITO'}), 200
    except Exception as e:
        logger.error('ERROR AL ACTUALIZAR LA INFORMACION')
        return jsonify({'error': 'ERROR AL ACTUALIZAR LA INFORMACION'}), 500


@app.route('/exist', methods=['GET'])
def existe():
    try:
        logger.info('Validacion de existencia de usuario iniciada')
        email = request.args.get('email', '')

        user_id = existUser(email)

        if user_id is None:
            return jsonify({'error': 'ERROR. CORREO NO VÁLIDO'}), 405

        user_id = user_id[0]

        logger.info('Validacion de existencia finalizada')
        return jsonify({'id': user_id}), 200

    except Exception as e:
        logger.error(e)
        return jsonify({'error': 'ERROR AL OBTENER EL ID'}), 405