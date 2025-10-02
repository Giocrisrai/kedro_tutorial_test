#!/bin/bash

# ===========================================
# SCRIPT DE INICIO PARA DESARROLLO
# ===========================================

echo "🚀 Iniciando Spaceflights - Entorno de DESARROLLO"
echo "=================================================="

# Verificar que Docker esté corriendo
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker no está corriendo. Por favor inicia Docker Desktop."
    exit 1
fi

# Construir imágenes si es necesario
echo "🔨 Construyendo imágenes Docker..."
docker-compose --profile development build

# Iniciar servicios de desarrollo
echo "🛠️  Iniciando servicios de desarrollo..."
docker-compose --profile development up -d

# Esperar a que los servicios estén listos
echo "⏳ Esperando a que los servicios estén listos..."
sleep 10

# Verificar estado de los servicios
echo "📊 Estado de los servicios:"
docker-compose --profile development ps

echo ""
echo "✅ Servicios de desarrollo iniciados:"
echo "   📊 JupyterLab: http://localhost:8888"
echo "   📈 Kedro Viz: http://localhost:4141"
echo ""
echo "💡 Comandos útiles:"
echo "   Ver logs: docker-compose --profile development logs -f"
echo "   Detener: docker-compose --profile development down"
echo "   Acceso interactivo: docker-compose exec jupyter-lab bash"
echo "   Ejecutar pipeline: docker-compose exec jupyter-lab kedro run"
echo ""
echo "🎉 ¡Entorno de desarrollo listo!"
