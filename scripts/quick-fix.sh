#!/bin/bash
set -e

echo "🔧 Aplicando Quick Fixes para Spaceflights..."
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fix 1: Crear network
echo -e "${YELLOW}1️⃣ Creando Docker network...${NC}"
if docker network create spaceflights-network 2>/dev/null; then
    echo -e "${GREEN}✓ Network 'spaceflights-network' creada${NC}"
else
    echo -e "${GREEN}✓ Network 'spaceflights-network' ya existe${NC}"
fi
echo ""

# Fix 2: Eliminar notebooks temporales
echo -e "${YELLOW}2️⃣ Eliminando notebooks temporales...${NC}"
if rm -f notebooks/Untitled.ipynb notebooks/Untitled1.ipynb 2>/dev/null; then
    echo -e "${GREEN}✓ Notebooks temporales eliminados${NC}"
else
    echo -e "${GREEN}✓ No hay notebooks temporales para eliminar${NC}"
fi
echo ""

# Fix 3: Crear .dockerignore si no existe
echo -e "${YELLOW}3️⃣ Verificando .dockerignore...${NC}"
if [ ! -f .dockerignore ]; then
    cat > .dockerignore << 'DOCKERIGNORE'
# Git
.git
.gitignore
.gitattributes

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/

# Virtual environments
.env
.venv
venv/
ENV/
env.bak/
venv.bak/

# Data directories
data/01_raw/
data/02_intermediate/
data/03_primary/
data/04_feature/
data/05_model_input/
data/06_models/
data/07_model_output/
data/08_reporting/

# Logs and temp
logs/
sessions/
*.log
backups/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Documentation (not needed in images)
*.md
docs/
README*

# Tests
tests/
.pytest_cache/
.coverage
.coverage.*
htmlcov/
.tox/
.nox/

# Notebooks
notebooks/.ipynb_checkpoints
notebooks/Untitled*.ipynb

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# UV lock
uv.lock

# DVC
.dvc/
.dvcignore

# Docker
docker-compose.override.yml
DOCKERIGNORE
    echo -e "${GREEN}✓ .dockerignore creado${NC}"
else
    echo -e "${GREEN}✓ .dockerignore ya existe${NC}"
fi
echo ""

# Fix 4: Verificar y crear .env si no existe
echo -e "${YELLOW}4️⃣ Verificando archivo .env...${NC}"
if [ ! -f .env ]; then
    if [ -f env.example ]; then
        cp env.example .env
        echo -e "${GREEN}✓ .env creado desde env.example${NC}"
        echo -e "${RED}⚠️  IMPORTANTE: Edita .env y configura credenciales seguras${NC}"
    else
        echo -e "${RED}❌ No se encontró env.example${NC}"
    fi
else
    echo -e "${GREEN}✓ .env ya existe${NC}"
fi
echo ""

# Fix 5: Crear directorios necesarios
echo -e "${YELLOW}5️⃣ Creando directorios necesarios...${NC}"
mkdir -p data/{01_raw,02_intermediate,03_primary,04_feature,05_model_input,06_models,07_model_output,08_reporting}
mkdir -p logs sessions backups
echo -e "${GREEN}✓ Directorios creados${NC}"
echo ""

# Fix 6: Ajustar permisos
echo -e "${YELLOW}6️⃣ Ajustando permisos de directorios...${NC}"
if chmod +x scripts/*.sh 2>/dev/null; then
    echo -e "${GREEN}✓ Scripts marcados como ejecutables${NC}"
fi
if chmod -R 755 data logs sessions 2>/dev/null; then
    echo -e "${GREEN}✓ Permisos de directorios ajustados${NC}"
fi
echo ""

# Fix 7: Verificar Docker está corriendo
echo -e "${YELLOW}7️⃣ Verificando Docker está corriendo...${NC}"
if docker info > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Docker está corriendo${NC}"
else
    echo -e "${RED}❌ Docker no está corriendo. Por favor inicia Docker Desktop.${NC}"
    exit 1
fi
echo ""

echo -e "${GREEN}✅ Quick Fixes aplicados exitosamente!${NC}"
echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}⚠️  ACCIONES MANUALES REQUERIDAS:${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "1. 🔑 Generar Fernet Key para Airflow:"
echo "   python3 -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\""
echo "   Luego agregar a .env: AIRFLOW_FERNET_KEY=<key-generada>"
echo ""
echo "2. 🔐 Editar .env y configurar contraseñas seguras:"
echo "   nano .env"
echo ""
echo "3. 🐳 Actualizar docker-compose.airflow.yml:"
echo "   Línea 155-156: Cambiar 'external: true' por solo:"
echo "   networks:"
echo "     spaceflights-network:"
echo ""
echo "4. 📅 Actualizar fechas en DAGs de Airflow:"
echo "   dags/spaceflights_dag.py línea 52"
echo "   Cambiar start_date=datetime(2023,1,1) a fecha actual"
echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "🚀 Próximos pasos:"
echo "   1. Completar acciones manuales arriba"
echo "   2. ./start.sh development"
echo "   3. Abrir http://localhost:8888 (JupyterLab)"
echo "   4. Abrir http://localhost:4141 (Kedro Viz)"
echo ""
echo "📚 Ver QUICK_FIXES.md para más detalles"

