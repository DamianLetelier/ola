#!/bin/bash
# Script de construcción para Railway

echo "Iniciando proceso de construcción..."

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Recolectar archivos estáticos
python manage.py collectstatic --noinput

echo "Construcción completada." 