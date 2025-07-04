# Usa imagen base liviana
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar solo lo necesario
COPY requirements-prod.txt .

# Crear entorno virtual e instalar dependencias limpias
RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements-prod.txt

# Copiar el resto del proyecto
COPY . .

# Agregar entorno al PATH
ENV PATH="/opt/venv/bin:$PATH"

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["gunicorn", "Crud_Damian.wsgi:application", "--bind", "0.0.0.0:8000"] 