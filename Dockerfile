FROM python:3.11-slim

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

# Copiar solo requirements-prod.txt, NO requirements.txt
COPY requirements-prod.txt .

# Instalar SOLO las dependencias livianas
RUN pip install --upgrade pip && pip install -r requirements-prod.txt

# Copiar el resto del proyecto después de la instalación
COPY . .

# Expone el puerto correcto para Railway (usualmente 8080)
EXPOSE 8080

CMD ["gunicorn", "Crud_Damian.wsgi:application", "--bind", "0.0.0.0:8080"]
