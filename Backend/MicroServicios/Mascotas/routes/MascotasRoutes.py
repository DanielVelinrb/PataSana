from flask import Blueprint, request, jsonify
from database.dbConnection import postgresql_connection
import hashlib, uuid, json, jwt
import uuid

app = Blueprint('mascotas_blueprint', __name__)

