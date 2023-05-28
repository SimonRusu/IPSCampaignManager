# Empezamos descargando la imagen de Python
FROM python:3.11-alpine

# Establecemos el directorio de trabajo
WORKDIR /app

# Instalamos las dependencias de compilación y OpenBLAS
RUN apk add --no-cache build-base libffi-dev openssl-dev gfortran openblas-dev

# Copiamos el archivo de requerimientos dentro de la imagen
COPY requirements.txt .

# Actualizamos pip
RUN pip install --upgrade pip

# Instalamos las dependencias especificadas en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código de la aplicación
COPY . .

# Exponemos el puerto deseado
EXPOSE 5000

# Establecemos el comando para ejecutar la aplicación
CMD ["python", "app.py"]
