FROM python:3.10-slim

# Exposa el port per HTTPS
EXPOSE 8443

WORKDIR /app

# Copia les dependències (requirements.txt) dins del contenidor
COPY requirements.txt /app/requirements.txt

# Instal·la les dependències necessàries
RUN pip install --no-cache-dir -r requirements.txt

# Copia tota l'aplicació FastAPI dins del contenidor
COPY . /app/


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "443", "--ssl-keyfile", "/app/ssl/key.pem", "--ssl-certfile", "/app/ssl/cert.pem"]