from flask import Blueprint, request, jsonify
import json, jwt
from repositories.visita_command_repository import registrar_visita
from repositories.visita_query_repository import listar_visitas
from datetime import datetime
from utils.usuarios_cliente import existUser
from logger import get_logger
logger = get_logger(__name__)

app = Blueprint('users_blueprint', __name__)


@app.route('/registrar', methods=['POST'])
def crearVisita():
    logger.info('Creacion de visita iniciada')
    data = request.json 
    fecha = data.get('fecha')
    duenio = data.get('duenio')
    observaciones = data.get('observaciones')
    nombre_mascota = data.get('nombre_mascota')
    token = request.headers.get('Authorization')
    
    if not token:
        return jsonify({'error': 'ERROR. TOKEN DE IDENTIFICACION REQUERIDO'}), 400
    
    if(fecha is None or duenio is None or observaciones is None or nombre_mascota is None):
        jsonify({'mensaje': 'CUERPO DE LA SOLICITUD INCORRECTO.'}), 400


    if not existUser(duenio):
        return jsonify({'mensaje': 'ERROR. EL USUARIO NO EXISTE'}), 400

    try:
        token = token.split(' ')[1]
        payload = jwt.decode(token, 'pan', algorithms=['HS256'])
        user_rol = payload['user_rol']
        user_id = payload['user_id']

        fecha = datetime.strptime(fecha, "%d/%m/%Y")
        resultado = registrar_visita(fecha, duenio, observaciones, nombre_mascota)

        if(resultado is None):
            return jsonify({'ERROR': 'ERROR AL REGISTRAR LA VISTA MÉDICA'}), 500

        logger.info('Creacion de visita finalizada')
        return jsonify({'message': 'Visita registrada con éxito'}), 200
    except ValueError as e:
        logger.error('Fecha ingresada invalida')
        logger.error(e)
        return jsonify({'FECHA INVALIDA': fecha}), 500
    except Exception as e:
         logger.error(e)
         return jsonify({'error': str(e)}), 500


@app.route('/listar', methods=['GET'])
def listar():
    logger.info('Listado de visitas iniciado')
    token = request.headers.get('Authorization')
    
    if not token:
        return jsonify({'error': 'ERROR. TOKEN DE IDENTIFICACION REQUERIDO'}), 400
    
    try:
        token = token.split(' ')[1]
        payload = jwt.decode(token, 'pan', algorithms=['HS256'])
        user_rol = payload['user_rol']
        user_id = payload['user_id']

        resultado = listar_visitas()

        if(resultado is None):
            return jsonify({'ERROR': 'ERROR AL LISTAR LAS VISITAS'}), 500

        logger.info('Listado de visitas finalizado')
        return jsonify({'visitas': resultado}), 200
    except Exception as e:
         logger.error(e)
         return jsonify({'error': str(e)}), 500