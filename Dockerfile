# Usar una imagen base de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requerimientos
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar la aplicación modular
COPY app/ ./app/

# Comando para ejecutar la aplicación
CMD ["python", "-u", "-m", "app.main"]

