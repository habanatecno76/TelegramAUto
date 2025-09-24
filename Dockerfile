# Usamos Python 3.11 por mayor compatibilidad con dependencias
FROM python:3.11-slim-bookworm

# Instalamos solo las dependencias del sistema necesarias
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Creamos directorio de trabajo (no necesitas mkdir para /app/sessions, se creará automáticamente)
WORKDIR /app

# Copiamos solo requirements.txt primero para mejor cacheo
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de la aplicación
COPY . .

# Configuración opcional para variables de entorno
ENV PYTHONUNBUFFERED=1

# Comando de inicio (aquí se creará /app/sessions si no existe)
CMD ["python", "main.py"]