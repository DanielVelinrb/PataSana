from database.dbConnection import postgresql_connection
import hashlib, uuid


def crear_usuario(nombre, email, password):
    try:
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        connection = postgresql_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO Usuario (ID, Nombre, Email, Password, Rol)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (str(uuid.uuid4()), nombre, email, password, "usuario",)
            )
        connection.commit()
        connection.close()
        return 200
    except Exception as e:
        return None


def cambiar_contrasenia_db(password, email):
    print("pan")
    try:
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        connection = postgresql_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE Usuario SET password = %s where email = %s
                """,
                (password, email)
            )
        connection.commit()
        connection.close()

        return 200
    except Exception as e:
        return None


def actualizar_db(id_usuario, nombre, email):
    try:
        connection = postgresql_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE Usuario SET email = %s, nombre = %s where id = %s
                """,
                (email, nombre, id_usuario, )
            )
        connection.commit()
        connection.close()

        return 200
    except Exception as e:
        print(e)
