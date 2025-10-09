#!/bin/bash
set -e

echo "🧹 Limpiando archivos basura del repositorio Spaceflights..."
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Contador de acciones
CLEANED=0

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  LIMPIEZA AUTOMÁTICA DE REPOSITORIO${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 1. Notebooks temporales
echo -e "${YELLOW}[1/8] Eliminando notebooks temporales...${NC}"
removed_notebooks=0
if [ -f "notebooks/Untitled.ipynb" ]; then
    rm -f notebooks/Untitled.ipynb
    ((removed_notebooks++))
fi
if [ -f "notebooks/Untitled1.ipynb" ]; then
    rm -f notebooks/Untitled1.ipynb
    ((removed_notebooks++))
fi
if [ $removed_notebooks -gt 0 ]; then
    echo -e "${GREEN}      ✓ $removed_notebooks notebook(s) temporal(es) eliminado(s)${NC}"
    ((CLEANED++))
else
    echo -e "${GREEN}      ✓ No hay notebooks temporales${NC}"
fi
echo ""

# 2. Directorio airflow_dags duplicado
echo -e "${YELLOW}[2/8] Verificando directorio airflow_dags duplicado...${NC}"
if [ -d "airflow_dags" ]; then
    echo -e "      ${RED}⚠️  Encontrado directorio duplicado 'airflow_dags/'${NC}"
    echo -e "      Este directorio duplica el contenido de 'dags/'"
    echo -n "      ¿Eliminar airflow_dags/? [y/N]: "
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        rm -rf airflow_dags/
        echo -e "${GREEN}      ✓ airflow_dags/ eliminado${NC}"
        ((CLEANED++))
    else
        echo -e "${YELLOW}      ⊘ Omitido por el usuario${NC}"
    fi
else
    echo -e "${GREEN}      ✓ No existe directorio duplicado${NC}"
fi
echo ""

# 3. Build artifacts
echo -e "${YELLOW}[3/8] Eliminando build artifacts...${NC}"
artifacts_removed=0
if [ -d "build" ]; then
    rm -rf build/
    echo -e "${GREEN}      ✓ build/ eliminado${NC}"
    ((artifacts_removed++))
fi
if [ -d "dist" ]; then
    rm -rf dist/
    echo -e "${GREEN}      ✓ dist/ eliminado${NC}"
    ((artifacts_removed++))
fi
if [ -d "src/spaceflights.egg-info" ]; then
    rm -rf src/spaceflights.egg-info/
    echo -e "${GREEN}      ✓ src/spaceflights.egg-info/ eliminado${NC}"
    ((artifacts_removed++))
fi
if [ $artifacts_removed -gt 0 ]; then
    ((CLEANED++))
else
    echo -e "${GREEN}      ✓ No hay build artifacts${NC}"
fi
echo ""

# 4. info.log
echo -e "${YELLOW}[4/8] Eliminando archivo info.log...${NC}"
if [ -f "info.log" ]; then
    rm -f info.log
    echo -e "${GREEN}      ✓ info.log eliminado${NC}"
    ((CLEANED++))
else
    echo -e "${GREEN}      ✓ info.log no existe${NC}"
fi
echo ""

# 5. __pycache__ directories
echo -e "${YELLOW}[5/8] Limpiando directorios __pycache__...${NC}"
pycache_count=$(find . -type d -name "__pycache__" 2>/dev/null | wc -l | tr -d ' ')
if [ "$pycache_count" -gt 0 ]; then
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    echo -e "${GREEN}      ✓ $pycache_count directorio(s) __pycache__ eliminado(s)${NC}"
    ((CLEANED++))
else
    echo -e "${GREEN}      ✓ No hay directorios __pycache__${NC}"
fi
echo ""

# 6. backups directory (con confirmación)
echo -e "${YELLOW}[6/8] Verificando directorio backups/...${NC}"
if [ -d "backups" ] && [ "$(ls -A backups 2>/dev/null)" ]; then
    backup_size=$(du -sh backups 2>/dev/null | cut -f1)
    echo -e "      ${RED}⚠️  Directorio backups/ contiene archivos (tamaño: $backup_size)${NC}"
    echo -n "      ¿Eliminar backups/? [y/N]: "
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        rm -rf backups/
        echo -e "${GREEN}      ✓ backups/ eliminado${NC}"
        ((CLEANED++))
    else
        echo -e "${YELLOW}      ⊘ Omitido por el usuario${NC}"
    fi
else
    echo -e "${GREEN}      ✓ backups/ vacío o no existe${NC}"
fi
echo ""

# 7. Limpiar logs antiguos (opcional)
echo -e "${YELLOW}[7/8] Logs antiguos...${NC}"
if [ -d "logs" ] && [ "$(find logs/ -type f -name '*.log' 2>/dev/null | wc -l | tr -d ' ')" -gt 0 ]; then
    old_logs=$(find logs/ -type f -name "*.log" -mtime +7 2>/dev/null | wc -l | tr -d ' ')
    if [ "$old_logs" -gt 0 ]; then
        echo -e "      Encontrados $old_logs log(s) antiguo(s) (>7 días)"
        echo -n "      ¿Limpiar logs antiguos? [y/N]: "
        read -r response
        if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            find logs/ -type f -name "*.log" -mtime +7 -delete 2>/dev/null || true
            echo -e "${GREEN}      ✓ Logs antiguos eliminados${NC}"
            ((CLEANED++))
        else
            echo -e "${YELLOW}      ⊘ Omitido por el usuario${NC}"
        fi
    else
        echo -e "${GREEN}      ✓ No hay logs antiguos (>7 días)${NC}"
    fi
else
    echo -e "${GREEN}      ✓ No hay logs para limpiar${NC}"
fi
echo ""

# 8. Verificar archivos en git que no deberían estar
echo -e "${YELLOW}[8/8] Verificando archivos en git que deberían ser ignorados...${NC}"
if git rev-parse --git-dir > /dev/null 2>&1; then
    git_cleaned=0
    
    # Verificar uv.lock
    if git ls-files 2>/dev/null | grep -q "^uv.lock$"; then
        git rm --cached uv.lock 2>/dev/null || true
        echo -e "${YELLOW}      ! uv.lock removido de git (commit pendiente)${NC}"
        ((git_cleaned++))
    fi
    
    # Verificar docker-compose.override.yml
    if git ls-files 2>/dev/null | grep -q "^docker-compose.override.yml$"; then
        git rm --cached docker-compose.override.yml 2>/dev/null || true
        echo -e "${YELLOW}      ! docker-compose.override.yml removido de git${NC}"
        ((git_cleaned++))
    fi
    
    # Verificar build/
    if git ls-files 2>/dev/null | grep -q "^build/"; then
        git rm -r --cached build/ 2>/dev/null || true
        echo -e "${YELLOW}      ! build/ removido de git${NC}"
        ((git_cleaned++))
    fi
    
    # Verificar dist/
    if git ls-files 2>/dev/null | grep -q "^dist/"; then
        git rm -r --cached dist/ 2>/dev/null || true
        echo -e "${YELLOW}      ! dist/ removido de git${NC}"
        ((git_cleaned++))
    fi
    
    # Verificar info.log
    if git ls-files 2>/dev/null | grep -q "^info.log$"; then
        git rm --cached info.log 2>/dev/null || true
        echo -e "${YELLOW}      ! info.log removido de git${NC}"
        ((git_cleaned++))
    fi
    
    if [ $git_cleaned -gt 0 ]; then
        echo -e "${GREEN}      ✓ $git_cleaned archivo(s) removido(s) de git${NC}"
        ((CLEANED++))
    else
        echo -e "${GREEN}      ✓ No hay archivos mal trackeados en git${NC}"
    fi
else
    echo -e "${YELLOW}      ⊘ No es un repositorio git${NC}"
fi

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Limpieza completada exitosamente!${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "   ${GREEN}✓${NC} Categorías procesadas: 8"
echo -e "   ${GREEN}✓${NC} Acciones de limpieza realizadas: $CLEANED"
echo ""

# Mostrar tamaño del directorio
if command -v du &> /dev/null; then
    repo_size=$(du -sh . 2>/dev/null | cut -f1)
    echo -e "   📊 Tamaño actual del repositorio: ${BLUE}$repo_size${NC}"
    echo ""
fi

echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}📝 PRÓXIMOS PASOS:${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "1. Revisar cambios en git:"
echo "   ${BLUE}git status${NC}"
echo ""
echo "2. Si hay archivos staged para remover:"
echo "   ${BLUE}git commit -m 'chore: Remove ignored files from git tracking'${NC}"
echo ""
echo "3. Limpiar versiones antiguas de modelos (opcional):"
echo "   ${BLUE}./scripts/clean-old-versions.sh${NC}"
echo ""
echo "4. Verificar que todo funciona:"
echo "   ${BLUE}./start.sh development${NC}"
echo ""
echo -e "${GREEN}📚 Ver LIMPIEZA_ARCHIVOS.md para más detalles${NC}"

