# Usa una imagen Python liviana
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia solo lo necesario
COPY requirements-prod.txt requirements.txt
COPY . .

# Crea entorno virtual e instala dependencias
RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Agrega el entorno al PATH
ENV PATH="/opt/venv/bin:$PATH"

# Expone el puerto
EXPOSE 8000

# Comando de inicio
CMD ["gunicorn", "Crud_Damian.wsgi:application", "--bind", "0.0.0.0:8000"] 