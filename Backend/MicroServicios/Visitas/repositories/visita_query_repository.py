from database.dbConnection import postgresql_connection

def listar_visitas():
    try:
        connection = postgresql_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM Visitas
                """
            )
            visitas = cursor.fetchall()
        connection.commit()
        connection.close()
        return visitas
    except Exception as e:
        print(e)
        return None