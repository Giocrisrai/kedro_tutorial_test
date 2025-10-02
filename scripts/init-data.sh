#!/bin/bash

# Script para inicializar datos de ejemplo en el proyecto Kedro
# Este script se ejecuta dentro del contenedor

set -e

echo "🚀 Inicializando datos de ejemplo para Spaceflights..."

# Crear directorios de datos si no existen
mkdir -p /app/data/01_raw
mkdir -p /app/data/02_intermediate
mkdir -p /app/data/03_primary
mkdir -p /app/data/04_feature
mkdir -p /app/data/05_model_input
mkdir -p /app/data/06_models
mkdir -p /app/data/07_model_output
mkdir -p /app/data/08_reporting

# Crear directorios de logs y sesiones
mkdir -p /app/logs
mkdir -p /app/sessions

# Verificar que Kedro esté configurado correctamente
echo "📋 Verificando configuración de Kedro..."
kedro info

# Ejecutar pipeline de datos de ejemplo si los datos no existen
if [ ! -f "/app/data/01_raw/companies.csv" ]; then
    echo "📊 Generando datos de ejemplo..."
    # Aquí podrías agregar comandos para generar datos de ejemplo
    # Por ahora, solo creamos archivos vacíos como placeholder
    touch /app/data/01_raw/companies.csv
    touch /app/data/01_raw/reviews.csv
    touch /app/data/01_raw/shuttles.xlsx
    echo "✅ Archivos de datos de ejemplo creados"
else
    echo "✅ Los datos ya existen, saltando generación"
fi

# Verificar permisos
chown -R kedro:kedro /app/data
chown -R kedro:kedro /app/logs
chown -R kedro:kedro /app/sessions

echo "🎉 Inicialización completada!"
