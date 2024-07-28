from database.dbConnection import postgresql_connection

def obtener_total_mascotas():
    try:
        connection = postgresql_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM MASCOTA 
                """                
            )
            mascotas = cursor.fetchall()
        connection.commit()
        connection.close()
        return mascotas
    except Exception as e:
        return 500


def obtener_mascotas_usuario(user_id):
    try:
        connection = postgresql_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM MASCOTA where id_dueno = %s
                """ ,
                (user_id, )                   
            )
            mascotas = cursor.fetchall()
        connection.commit()
        connection.close()
        return mascotas
    except Exception as e:
        return 500


def obtener_info_mascota_db(user_id, nombre):
    try:
        connection = postgresql_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM MASCOTA where id_dueno = %s and nombre = %s
                """ ,
                (user_id, nombre, )               
            )
                    
            mascota = cursor.fetchone()
        connection.commit()
        connection.close()

        if mascota is None:
            return 400
        return mascota
    except Exception as e:
        print(e)
        return 500


def mascotas_por_usuario():
    try:
        connection = postgresql_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id_dueno, count(*) FROM MASCOTA 
                GROUP BY id_dueno
                """            
            )
                    
            conteo_mascotas = cursor.fetchall()
        connection.commit()
        connection.close()

        return {id_dueno: count for id_dueno, count in conteo_mascotas}
    except Exception as e:
        print(e)
        return 500