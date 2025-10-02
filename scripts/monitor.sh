#!/bin/bash

# ===========================================
# SCRIPT DE MONITOREO
# ===========================================

ENVIRONMENT=${1:-development}

echo "📊 Monitoreo de Spaceflights - Entorno: $ENVIRONMENT"
echo "=================================================="

# Verificar que el entorno sea válido
if [[ "$ENVIRONMENT" != "development" && "$ENVIRONMENT" != "production" ]]; then
    echo "❌ Error: Entorno debe ser 'development' o 'production'"
    exit 1
fi

PROFILE=$ENVIRONMENT

echo "🔍 Estado de los contenedores:"
echo "================================"
docker-compose --profile $PROFILE ps

echo ""
echo "📈 Uso de recursos:"
echo "==================="
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}" $(docker-compose --profile $PROFILE ps -q)

echo ""
echo "📋 Logs recientes (últimas 10 líneas):"
echo "======================================"
docker-compose --profile $PROFILE logs --tail=10

echo ""
echo "💡 Comandos de monitoreo:"
echo "   Ver logs en tiempo real: docker-compose --profile $PROFILE logs -f"
echo "   Ver logs de un servicio: docker-compose logs -f [nombre_servicio]"
echo "   Ver estadísticas: docker stats"
echo "   Acceso al contenedor: docker-compose exec [nombre_servicio] bash"
