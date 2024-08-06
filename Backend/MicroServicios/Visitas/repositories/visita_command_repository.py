from database.dbConnection import postgresql_connection
import hashlib, uuid

def registrar_visita(fecha, duenio, observaciones, nombre_mascota):
    try:
        connection = postgresql_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO Visitas (Id, Fecha, Duenio, Observaciones, Nombremascota)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (str(uuid.uuid4()), fecha, duenio, observaciones, nombre_mascota,)
            )
        connection.commit()
        connection.close()
        return 200
    except Exception as e:
        print(e)
        return None