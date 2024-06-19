# Usa una imagen base oficial de Python
FROM python:3.11

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de requerimientos al contenedor
COPY requirements.txt .

# Instala las dependencias
RUN pip install --verbose -r requirements.txt

# Copia el contenido de tu proyecto al directorio de trabajo
COPY Backend/pataSana /app
COPY Frontend /app/Frontend

# Configuración para manejar archivos estáticos
RUN mkdir -p /app/staticfiles/
RUN mkdir -p /app/media/

# Recoge archivos estáticos
RUN python manage.py collectstatic --noinput

# Expone el puerto en el que Django correrá
EXPOSE 8000

# Comando para correr la aplicación Django
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "pataSana.wsgi:application"]
