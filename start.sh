#!/bin/bash

# Script de inicio rápido para Spaceflights Docker
# Uso: ./start.sh [profile]

set -e

PROFILE=${1:-"development"}

echo "🚀 Iniciando Spaceflights con perfil: $PROFILE"

# Verificar que Docker esté corriendo
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker no está corriendo. Por favor inicia Docker Desktop."
    exit 1
fi

# Verificar que el archivo .env existe
if [ ! -f ".env" ]; then
    echo "📋 Creando archivo .env desde template..."
    cp env.example .env
    echo "✅ Archivo .env creado. Puedes editarlo según tus necesidades."
fi

# Construir imágenes si es necesario
echo "🔨 Construyendo imágenes Docker..."
docker-compose build

# Levantar servicios según el perfil
case $PROFILE in
    "development")
        echo "🛠️  Iniciando entorno de desarrollo..."
        docker-compose --profile development up -d
        echo ""
        echo "✅ Servicios iniciados:"
        echo "   📊 JupyterLab: http://localhost:8888"
        echo "   📈 Kedro Viz: http://localhost:4141"
        echo ""
        echo "💡 Comandos útiles:"
        echo "   Ver logs: docker-compose logs -f"
        echo "   Detener: docker-compose down"
        echo "   Acceso interactivo: docker-compose exec jupyter-lab bash"
        ;;
    "production")
        echo "🏭 Iniciando entorno de producción..."
        docker-compose --profile production up -d
        echo "✅ Servicios de producción iniciados"
        ;;
    "full")
        echo "🌟 Iniciando stack completo..."
        docker-compose --profile development --profile database --profile cache up -d
        echo ""
        echo "✅ Stack completo iniciado:"
        echo "   📊 JupyterLab: http://localhost:8888"
        echo "   📈 Kedro Viz: http://localhost:4141"
        echo "   🗄️  PostgreSQL: localhost:5432"
        echo "   🔄 Redis: localhost:6379"
        ;;
    *)
        echo "❌ Perfil no válido: $PROFILE"
        echo "Perfiles disponibles: development, production, full"
        exit 1
        ;;
esac

echo ""
echo "🎉 ¡Spaceflights está listo para usar!"
