from database.dbConnection import postgresql_connection

def registrar_mascota_db(mascota_id, nombre, raza, especie, edad, observaciones, duenio):
    try:
        connection = postgresql_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO MASCOTA (ID, Nombre, Raza, Especie, Edad, Observaciones, id_dueno)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (mascota_id, nombre, raza, especie, edad, observaciones, duenio, )
            )
                
        connection.commit()
        connection.close()
        return 200
    except Exception as e:
        print(e)
        return None

def borrar_registro_mascota(duenio, nombre):
    try:
        connection = postgresql_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM MASCOTA where id_dueno = %s and nombre = %s
                """,
                (duenio, nombre)
            )
            
        connection.commit()
        connection.close()
        return 200
    except Exception as e:
        print(e)
        return None


def actualizar_registro_mascota(nombre, raza, especie, edad, observaciones, id_mascota):
    try:
        connection = postgresql_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE MASCOTA SET 
                nombre = %s, raza = %s, especie = %s, edad = %s, observaciones = %s
                where id = %s
                """,
                (nombre, raza, especie, edad, observaciones, id_mascota, )
            )
            
        connection.commit()
        connection.close()
        return 200
    except Exception as e:
        print(e)
        return None