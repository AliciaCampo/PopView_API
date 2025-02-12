# Usa una imagen base con Python
FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de requisitos e instala las dependencias
COPY API/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código fuente al contenedor
COPY API /app/

# Expón el puerto que la aplicación utilizará (puerto para HTTPS)
EXPOSE 8443

# Comando para iniciar la aplicación FastAPI con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8443", "--ssl-keyfile", "/app/ssl/key.pem", "--ssl-certfile", "/app/ssl/cert.pem"]
