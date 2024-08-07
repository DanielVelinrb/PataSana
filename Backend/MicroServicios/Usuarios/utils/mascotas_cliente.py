import requests

def mascotas_por_usuario(token):
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get('http://172.20.0.3:8082/mascotas/conteo', headers=headers)

        if response.status_code == 200:
            mascotas = response.json()
            return mascotas.get('resultado')
        return None
    except Exception as e:
        print(e)