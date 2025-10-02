#!/bin/bash

# ===========================================
# SCRIPT DE INICIO PARA PRODUCCIÓN
# ===========================================

echo "🚀 Iniciando Spaceflights - Entorno de PRODUCCIÓN"
echo "=================================================="

# Verificar que Docker esté corriendo
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker no está corriendo. Por favor inicia Docker Desktop."
    exit 1
fi

# Construir imágenes si es necesario
echo "🔨 Construyendo imágenes Docker..."
docker-compose --profile production build

# Iniciar servicios de producción
echo "🛠️  Iniciando servicios de producción..."
docker-compose --profile production up -d

# Esperar a que los servicios estén listos
echo "⏳ Esperando a que los servicios estén listos..."
sleep 15

# Verificar estado de los servicios
echo "📊 Estado de los servicios:"
docker-compose --profile production ps

echo ""
echo "✅ Servicios de producción iniciados:"
echo "   🏭 Kedro Producción: Ejecutando pipelines automáticamente"
echo "   ⏰ Scheduler: Ejecutando cada hora"
echo "   📈 Kedro Viz: http://localhost:4141"
echo ""
echo "💡 Comandos útiles:"
echo "   Ver logs: docker-compose --profile production logs -f"
echo "   Ver logs del scheduler: docker-compose logs -f kedro-scheduler"
echo "   Detener: docker-compose --profile production down"
echo "   Ejecutar pipeline manual: docker-compose exec kedro-prod kedro run"
echo ""
echo "🎉 ¡Entorno de producción listo!"
