#Ejecutar back
python manage.py runserver

#Connection String
PGPASSWORD=jZsWlebHkpoFcxWumtidgPWhWEZlETwj psql -h monorail.proxy.rlwy.net -U postgres -p 51331 -d railway


#Requerimientos psycopg2

Credenciales de admin:
Correo: dios@example.com
Contraseña: dios

#USUARIOS
Crear usuario: Se valida que el correo no se encuentre registrado para crear o no el registro.
No se almacena la contraseña, mas bien se almacena su valor HASH. Todos los usuarios creados 
tienen el rol administrador por default. 

Login: Para loguearse se validan las credenciales. En caso de ser credenciales válidas se genera
un JWT, actualmente únicamente posee la id del usuario y el rol

Cambiar contraseña: Se valida que el usuario exista.

#Mascotas
Crear mascota: Esta funcionalidad está pensada desde el rol de admin, entre los atributos del 
request se debe pasar el correo del dueño de la mascota. Se valida que el dueño exista, que el
rol del usuario que realiza el query sea "admin" y que no exista una mascota con ese nombre 
asociada a dicho usuario. 

Borrar mascota: Esta funcionalidad está pensada desde el rol de admin, entre los atributos del 
request se debe pasar el correo del dueño de la mascota. Se valida que el dueño exista, que el
rol del usuario que realiza el query sea "admin" y que exista una mascota con ese nombre.