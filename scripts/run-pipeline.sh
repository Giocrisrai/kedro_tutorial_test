#!/bin/bash

# ===========================================
# SCRIPT PARA EJECUTAR PIPELINES
# ===========================================

ENVIRONMENT=${1:-development}
PIPELINE=${2:-all}

echo "🚀 Ejecutando pipeline en entorno: $ENVIRONMENT"
echo "📊 Pipeline: $PIPELINE"
echo "=============================================="

# Verificar que el entorno sea válido
if [[ "$ENVIRONMENT" != "development" && "$ENVIRONMENT" != "production" ]]; then
    echo "❌ Error: Entorno debe ser 'development' o 'production'"
    echo "Uso: $0 [development|production] [pipeline_name]"
    exit 1
fi

# Determinar el comando según el entorno
if [[ "$ENVIRONMENT" == "development" ]]; then
    CONTAINER="jupyter-lab"
    PROFILE="development"
else
    CONTAINER="kedro-prod"
    PROFILE="production"
fi

# Verificar que el contenedor esté corriendo
if ! docker-compose --profile $PROFILE ps | grep -q "$CONTAINER.*Up"; then
    echo "❌ Error: El contenedor $CONTAINER no está corriendo en el entorno $ENVIRONMENT"
    echo "💡 Inicia el entorno primero con: ./scripts/start-$ENVIRONMENT.sh"
    exit 1
fi

# Ejecutar el pipeline
if [[ "$PIPELINE" == "all" ]]; then
    echo "🔄 Ejecutando pipeline completo..."
    docker-compose --profile $PROFILE exec $CONTAINER kedro run
else
    echo "🔄 Ejecutando pipeline: $PIPELINE"
    docker-compose --profile $PROFILE exec $CONTAINER kedro run --pipeline $PIPELINE
fi

echo "✅ Pipeline ejecutado exitosamente"