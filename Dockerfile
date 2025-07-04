# Usa una imagen base liviana
FROM python:3.11-slim

# Crea y activa entorno virtual
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Establece directorio de trabajo
WORKDIR /app

# Copia solo los archivos necesarios primero (para cache)
COPY requirements-prod.txt .

# Instala solo dependencias esenciales
RUN pip install --upgrade pip && pip install -r requirements-prod.txt

# Copia el resto del proyecto (NO requirements.txt)
COPY . .

# Expone el puerto correcto
EXPOSE 8080

# Comando de ejecución
CMD ["gunicorn", "Crud_Damian.wsgi:application", "--bind", "0.0.0.0:8080"] 