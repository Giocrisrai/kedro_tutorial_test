#!/bin/bash

# ===========================================
# SCRIPT DE GESTIÓN DE BASE DE DATOS
# Spaceflights PostgreSQL
# ===========================================

ACTION=${1:-status}
ENVIRONMENT=${2:-production}

echo "🗄️  Gestión de Base de Datos Spaceflights"
echo "=========================================="
echo "Acción: $ACTION"
echo "Entorno: $ENVIRONMENT"
echo ""

case $ACTION in
    "start")
        echo "🚀 Iniciando base de datos PostgreSQL..."
        docker-compose --profile $ENVIRONMENT up -d postgres
        echo "⏳ Esperando a que la base de datos esté lista..."
        sleep 10
        echo "✅ Base de datos iniciada en puerto 5433"
        ;;
    
    "stop")
        echo "🛑 Deteniendo base de datos PostgreSQL..."
        docker-compose --profile $ENVIRONMENT stop postgres
        echo "✅ Base de datos detenida"
        ;;
    
    "restart")
        echo "🔄 Reiniciando base de datos PostgreSQL..."
        docker-compose --profile $ENVIRONMENT restart postgres
        echo "✅ Base de datos reiniciada"
        ;;
    
    "status")
        echo "📊 Estado de la base de datos:"
        docker-compose --profile $ENVIRONMENT ps postgres
        echo ""
        echo "🔍 Verificando conexión..."
        if docker-compose --profile $ENVIRONMENT exec postgres pg_isready -U kedro -d spaceflights; then
            echo "✅ Base de datos conectada y funcionando"
        else
            echo "❌ Base de datos no disponible"
        fi
        ;;
    
    "logs")
        echo "📋 Logs de la base de datos:"
        docker-compose --profile $ENVIRONMENT logs -f postgres
        ;;
    
    "connect")
        echo "🔌 Conectando a la base de datos..."
        echo "Host: localhost"
        echo "Puerto: 5433"
        echo "Base de datos: spaceflights"
        echo "Usuario: kedro"
        echo "Contraseña: kedro123"
        echo ""
        echo "Usando psql..."
        docker-compose --profile $ENVIRONMENT exec postgres psql -U kedro -d spaceflights
        ;;
    
    "backup")
        BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).sql"
        echo "💾 Creando respaldo de la base de datos..."
        docker-compose --profile $ENVIRONMENT exec postgres pg_dump -U kedro spaceflights > "backups/$BACKUP_FILE"
        echo "✅ Respaldo creado: backups/$BACKUP_FILE"
        ;;
    
    "restore")
        BACKUP_FILE=${2:-""}
        if [ -z "$BACKUP_FILE" ]; then
            echo "❌ Error: Especifica el archivo de respaldo"
            echo "Uso: $0 restore <archivo_backup>"
            exit 1
        fi
        echo "🔄 Restaurando base de datos desde: $BACKUP_FILE"
        docker-compose --profile $ENVIRONMENT exec -T postgres psql -U kedro -d spaceflights < "backups/$BACKUP_FILE"
        echo "✅ Base de datos restaurada"
        ;;
    
    "reset")
        echo "⚠️  ADVERTENCIA: Esto eliminará todos los datos"
        read -p "¿Estás seguro? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "🗑️  Eliminando datos existentes..."
            docker-compose --profile $ENVIRONMENT down postgres
            docker volume rm spaceflights_postgres_data 2>/dev/null || true
            echo "🔄 Reiniciando base de datos..."
            docker-compose --profile $ENVIRONMENT up -d postgres
            echo "✅ Base de datos reiniciada con datos limpios"
        else
            echo "❌ Operación cancelada"
        fi
        ;;
    
    *)
        echo "❌ Acción no válida: $ACTION"
        echo ""
        echo "💡 Acciones disponibles:"
        echo "   start     - Iniciar base de datos"
        echo "   stop      - Detener base de datos"
        echo "   restart   - Reiniciar base de datos"
        echo "   status    - Ver estado de la base de datos"
        echo "   logs      - Ver logs de la base de datos"
        echo "   connect   - Conectar a la base de datos"
        echo "   backup    - Crear respaldo de la base de datos"
        echo "   restore   - Restaurar desde respaldo"
        echo "   reset     - Reiniciar base de datos (elimina datos)"
        echo ""
        echo "Uso: $0 <acción> [entorno]"
        echo "Ejemplo: $0 start production"
        exit 1
        ;;
esac
