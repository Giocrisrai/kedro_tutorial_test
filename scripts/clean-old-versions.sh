#!/bin/bash
set -e

echo "🗂️  Limpiando versiones antiguas de modelos y reportes..."
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

KEEP_VERSIONS=2  # Mantener las 2 versiones más recientes

clean_versioned_dir() {
    local dir=$1
    local name=$(basename "$dir")
    
    if [ ! -d "$dir" ]; then
        return
    fi
    
    # Contar versiones
    version_count=$(ls -1 "$dir" 2>/dev/null | wc -l | tr -d ' ')
    
    if [ "$version_count" -eq 0 ]; then
        echo -e "  ${YELLOW}⊘${NC} $name: vacío"
        return
    fi
    
    if [ "$version_count" -le "$KEEP_VERSIONS" ]; then
        echo -e "  ${GREEN}✓${NC} $name: $version_count versión(es) - manteniendo todas"
        return
    fi
    
    echo -e "  ${BLUE}📦${NC} $name: $version_count versión(es) encontradas"
    
    # Calcular cuántas eliminar
    to_delete=$((version_count - KEEP_VERSIONS))
    
    # Eliminar versiones antiguas (mantener las más recientes)
    deleted=0
    ls -1t "$dir" | tail -n +$((KEEP_VERSIONS + 1)) | while read -r version; do
        rm -rf "$dir/$version"
        ((deleted++)) || true
    done
    
    echo -e "     ${GREEN}→${NC} Eliminadas $to_delete versión(es) antigua(s)"
    echo -e "     ${GREEN}→${NC} Mantenidas $KEEP_VERSIONS versión(es) más reciente(s)"
}

echo -e "${BLUE}Configuración:${NC} Mantener las $KEEP_VERSIONS versiones más recientes"
echo ""

# Limpiar modelos
if [ -d "data/06_models" ]; then
    echo -e "${YELLOW}📦 Limpiando modelos...${NC}"
    model_count=0
    for model_dir in data/06_models/*/; do
        if [ -d "$model_dir" ]; then
            clean_versioned_dir "$model_dir"
            ((model_count++))
        fi
    done
    if [ $model_count -eq 0 ]; then
        echo -e "  ${YELLOW}⊘${NC} No hay modelos para limpiar"
    fi
    echo ""
else
    echo -e "${YELLOW}⊘ Directorio data/06_models/ no existe${NC}"
    echo ""
fi

# Limpiar reportes
if [ -d "data/08_reporting" ]; then
    echo -e "${YELLOW}📊 Limpiando reportes...${NC}"
    report_count=0
    for report_dir in data/08_reporting/*/; do
        if [ -d "$report_dir" ]; then
            clean_versioned_dir "$report_dir"
            ((report_count++))
        fi
    done
    if [ $report_count -eq 0 ]; then
        echo -e "  ${YELLOW}⊘${NC} No hay reportes para limpiar"
    fi
    echo ""
else
    echo -e "${YELLOW}⊘ Directorio data/08_reporting/ no existe${NC}"
    echo ""
fi

echo -e "${GREEN}✅ Limpieza de versiones completada!${NC}"
echo ""

# Mostrar resumen de espacio
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}📊 RESUMEN DE ESPACIO:${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

if [ -d "data/06_models" ]; then
    echo "Modelos:"
    du -sh data/06_models/*/ 2>/dev/null | while read -r size path; do
        name=$(basename "$path")
        version_count=$(ls -1 "$path" 2>/dev/null | wc -l | tr -d ' ')
        echo "  • $name: $size ($version_count versión(es))"
    done
    echo ""
fi

if [ -d "data/08_reporting" ]; then
    echo "Reportes:"
    du -sh data/08_reporting/*/ 2>/dev/null | while read -r size path; do
        name=$(basename "$path")
        version_count=$(ls -1 "$path" 2>/dev/null | wc -l | tr -d ' ')
        echo "  • $name: $size ($version_count versión(es))"
    done
    echo ""
fi

total_data_size=$(du -sh data/ 2>/dev/null | cut -f1)
echo -e "Total data/: ${GREEN}$total_data_size${NC}"

