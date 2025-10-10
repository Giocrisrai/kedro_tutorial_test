#!/bin/bash

# Script de verificación rápida del proyecto Spaceflights
# Ejecuta validaciones básicas para asegurar que todo está funcionando

echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║           🔍 VERIFICACIÓN RÁPIDA - SPACEFLIGHTS MLOPS           ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

ERRORS=0

# Verificar Python
echo "🐍 Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "   ✅ $PYTHON_VERSION"
else
    echo "   ❌ Python 3 no encontrado"
    ERRORS=$((ERRORS + 1))
fi

# Verificar Docker
echo ""
echo "🐳 Verificando Docker..."
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    echo "   ✅ $DOCKER_VERSION"
else
    echo "   ❌ Docker no encontrado"
    ERRORS=$((ERRORS + 1))
fi

# Verificar DAGs
echo ""
echo "📊 Verificando DAGs..."
DAG_COUNT=$(ls -1 dags/*.py 2>/dev/null | grep -v -E "backup|config|__init__" | wc -l | tr -d ' ')
if [ "$DAG_COUNT" -eq 4 ]; then
    echo "   ✅ 4 DAGs encontrados"
    ls -1 dags/spaceflights_*.py | grep -v backup | while read f; do
        echo "      • $(basename $f)"
    done
else
    echo "   ⚠️  Se esperaban 4 DAGs, se encontraron $DAG_COUNT"
    ERRORS=$((ERRORS + 1))
fi

# Verificar datos
echo ""
echo "📁 Verificando datos raw..."
DATA_COUNT=$(ls -1 data/01_raw/*.{csv,xlsx} 2>/dev/null | wc -l | tr -d ' ')
if [ "$DATA_COUNT" -ge 3 ]; then
    echo "   ✅ $DATA_COUNT archivos de datos encontrados"
    ls -1 data/01_raw/*.{csv,xlsx} 2>/dev/null | while read f; do
        SIZE=$(ls -lh "$f" | awk '{print $5}')
        echo "      • $(basename $f) ($SIZE)"
    done
else
    echo "   ⚠️  Faltan archivos de datos (encontrados: $DATA_COUNT, esperados: 3)"
    ERRORS=$((ERRORS + 1))
fi

# Verificar estructura de pipelines
echo ""
echo "🔄 Verificando pipelines de Kedro..."
PIPELINE_COUNT=$(ls -d src/spaceflights/pipelines/*/ 2>/dev/null | grep -v __pycache__ | wc -l | tr -d ' ')
if [ "$PIPELINE_COUNT" -eq 3 ]; then
    echo "   ✅ 3 pipelines encontrados"
    echo "      • data_processing"
    echo "      • data_science"
    echo "      • reporting"
else
    echo "   ⚠️  Se esperaban 3 pipelines, se encontraron $PIPELINE_COUNT"
    ERRORS=$((ERRORS + 1))
fi

# Verificar documentación
echo ""
echo "📚 Verificando documentación..."
DOC_FILES=("README.md" "INFORME_VERIFICACION.md" "VERIFICACION_RAPIDA.md")
DOC_COUNT=0
for file in "${DOC_FILES[@]}"; do
    if [ -f "$file" ]; then
        DOC_COUNT=$((DOC_COUNT + 1))
        SIZE=$(ls -lh "$file" | awk '{print $5}')
        echo "   ✅ $file ($SIZE)"
    else
        echo "   ⚠️  $file no encontrado"
    fi
done

# Verificar scripts
echo ""
echo "🔧 Verificando scripts de validación..."
if [ -f "scripts/validate_dag_structure.py" ]; then
    echo "   ✅ validate_dag_structure.py"
else
    echo "   ⚠️  validate_dag_structure.py no encontrado"
    ERRORS=$((ERRORS + 1))
fi

if [ -f "scripts/test_dag_imports.py" ]; then
    echo "   ✅ test_dag_imports.py"
else
    echo "   ⚠️  test_dag_imports.py no encontrado"
    ERRORS=$((ERRORS + 1))
fi

# Ejecutar validación de DAGs
echo ""
echo "🔍 Ejecutando validación de estructura de DAGs..."
if [ -f "scripts/validate_dag_structure.py" ]; then
    python3 scripts/validate_dag_structure.py > /tmp/dag_validation.log 2>&1
    if [ $? -eq 0 ]; then
        echo "   ✅ Validación exitosa (ver detalles con: python3 scripts/validate_dag_structure.py)"
    else
        echo "   ⚠️  Validación con advertencias"
        ERRORS=$((ERRORS + 1))
    fi
fi

# Resumen final
echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "📊 RESUMEN"
echo "═══════════════════════════════════════════════════════════════════"

if [ $ERRORS -eq 0 ]; then
    echo ""
    echo "   🎉 ¡TODO CORRECTO! El proyecto está listo para usar."
    echo ""
    echo "   Próximos pasos:"
    echo "   1. ./start.sh airflow    → Iniciar Airflow"
    echo "   2. ./start.sh development → Iniciar desarrollo"
    echo "   3. Ver VERIFICACION_RAPIDA.md para más opciones"
    echo ""
    exit 0
else
    echo ""
    echo "   ⚠️  Se encontraron $ERRORS problemas."
    echo "   Por favor revisa los mensajes arriba."
    echo ""
    exit 1
fi

