from database.dbConnection import postgresql_connection
import json, requests


def existUser(email):
    try:
        url = 'http://172.20.0.2:8081/usuarios/exist'
        params = {'email': email}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            mascotas = response.json()
            return mascotas.get('id')

        return None
    except Exception as e:
        print(e)

