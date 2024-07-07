import psycopg2
import uuid

def postgresql_connection():
    try:
        conn = psycopg2.connect(
            host='monorail.proxy.rlwy.net',
            database='railway',
            user='postgres',
            password='jZsWlebHkpoFcxWumtidgPWhWEZlETwj',
            port='51331'
        )
        return conn  # Retorna la conexión si se estableció correctamente
    except psycopg2.Error as e:
        print(f"Error al conectar a PostgreSQL: {e}")