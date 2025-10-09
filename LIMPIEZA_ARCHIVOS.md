# 🧹 LIMPIEZA DE ARCHIVOS BASURA - SPACEFLIGHTS

## 🎯 Objetivo
Eliminar archivos innecesarios, duplicados y temporales que no deberían estar en el repositorio y que pueden generar confusión en los estudiantes.

---

## 🚨 ARCHIVOS BASURA IDENTIFICADOS

### 1️⃣ Notebooks Temporales (🔴 CRÍTICO)
**Eliminar inmediatamente**:
```
notebooks/Untitled.ipynb
notebooks/Untitled1.ipynb
```

**Razón**: Notebooks sin nombre, probablemente de pruebas, no aportan valor educativo.

**Acción**:
```bash
rm -f notebooks/Untitled.ipynb notebooks/Untitled1.ipynb
```

---

### 2️⃣ Directorio airflow_dags/ DUPLICADO (🔴 CRÍTICO)
**Problema**: Existe tanto `airflow_dags/` como `dags/` con los mismos archivos

**Directorios**:
```
airflow_dags/          # ❌ DUPLICADO
├── spaceflights_dag.py
├── spaceflights_data_processing_dag.py
└── spaceflights_reporting_dag.py

dags/                  # ✅ CORRECTO (usado por Airflow)
├── spaceflights_dag.py
├── spaceflights_data_processing_dag.py
└── spaceflights_reporting_dag.py
```

**Razón**: Confusión sobre cuál es el directorio correcto. Airflow usa `dags/`.

**Acción**:
```bash
# Verificar que son idénticos
diff -r airflow_dags/ dags/

# Eliminar duplicado
rm -rf airflow_dags/
```

---

### 3️⃣ Build Artifacts (🔴 CRÍTICO)
**Eliminar**:
```
build/                 # Artefactos de compilación
dist/                  # Artefactos de distribución
src/spaceflights.egg-info/  # Info de instalación
```

**Razón**: 
- Generados automáticamente por `pip install -e .`
- No deben estar en control de versiones
- Se regeneran en cada instalación
- Ocupan espacio innecesario

**Acción**:
```bash
rm -rf build/ dist/ src/spaceflights.egg-info/
```

**Verificar en .gitignore**:
```gitignore
build/
dist/
*.egg-info/
```

---

### 4️⃣ Directorio backups/ (🟡 REVISAR)
**Contenido**: Desconocido (no listado en scan)

**Razón posible eliminación**:
- Backups no deben estar en repo
- Ocupan espacio
- Git ya es el sistema de control de versiones

**Acción**:
```bash
# Primero revisar contenido
ls -la backups/

# Si son realmente backups, eliminar
rm -rf backups/
```

**Alternativa**: Si son backups importantes, mover a ubicación externa.

---

### 5️⃣ Logs de Airflow (🟡 PARCIAL)
**Problema**: `logs/` contiene logs de ejecuciones de Airflow

**Contenido**:
```
logs/
├── dag_processor_manager/
└── scheduler/
    ├── 2025-10-03/
    ├── 2025-10-04/
    ├── 2025-10-05/
    ├── 2025-10-06/
    └── 2025-10-07/
```

**Decisión**:
- ❌ NO eliminar el directorio logs/ (necesario para funcionamiento)
- ✅ Limpiar logs antiguos
- ✅ Mantener estructura
- ✅ Verificar está en .gitignore

**Acción**:
```bash
# Limpiar contenido pero mantener estructura
find logs/ -type f -name "*.log" -delete
# O mantener logs y solo verificar .gitignore
```

**Verificar en .gitignore**:
```gitignore
logs/
*.log
```

---

### 6️⃣ Archivo info.log (🔴 CRÍTICO)
**Eliminar**:
```
info.log               # Log en raíz del proyecto
```

**Razón**: 
- Log individual que no debería estar commitado
- Información temporal de ejecución
- Ya existe directorio logs/ para esto

**Acción**:
```bash
rm -f info.log
```

**Verificar en .gitignore**:
```gitignore
*.log
```

---

### 7️⃣ uv.lock (🟢 OK - Ya en .gitignore)
**Estado**: Ya está en .gitignore según README

**Verificación necesaria**:
```bash
# Si está commitado, eliminarlo
git rm --cached uv.lock
```

**Acción**: Solo si está en git:
```bash
git rm --cached uv.lock
git commit -m "Remove uv.lock from version control"
```

---

### 8️⃣ docker-compose.override.yml (🟢 OK - Ya en .gitignore)
**Estado**: Ya está en .gitignore

**Verificación necesaria**:
```bash
# Si está commitado, eliminarlo
git rm --cached docker-compose.override.yml
```

---

### 9️⃣ __pycache__ Directories (🟡 NORMAL)
**Ubicaciones**:
```
src/spaceflights/__pycache__/
dags/__pycache__/
tests/__pycache__/
... otros
```

**Estado**: 
- ✅ Normal que existan en desarrollo
- ✅ Ya están en .gitignore
- ❌ No deben estar en git

**Acción**:
```bash
# Limpiar todos
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# Verificar no están en git
git rm -r --cached **/__pycache__/ 2>/dev/null || true
```

---

### 🔟 sessions/ Directory (🟢 OK)
**Estado**: Directorio necesario para Kedro

**Acción**: 
- ✅ Mantener directorio
- ✅ Verificar está en .gitignore
- ❌ No commitear contenido

**Verificar en .gitignore**:
```gitignore
sessions/
```

---

### 1️⃣1️⃣ data/ con Datos Generados (🟡 REVISAR)
**Problema**: `data/` contiene múltiples versiones de modelos y reportes

**Contenido problemático**:
```
data/06_models/regressor.pickle/
├── 2025-08-20T23.24.39.892Z/
├── 2025-08-20T23.27.08.477Z/
├── 2025-10-02T22.24.02.478Z/
├── 2025-10-02T22.26.43.602Z/
├── 2025-10-02T22.28.31.006Z/
├── 2025-10-02T22.36.22.503Z/
└── 2025-10-02T22.36.54.243Z/    # 7 versiones!

data/08_reporting/
├── dummy_confusion_matrix.png/   # 6 versiones
├── shuttle_passenger_capacity_plot_exp.json/  # 6 versiones
└── shuttle_passenger_capacity_plot_go.json/   # 6 versiones
```

**Decisión**:
- ❌ No commitear estas versiones (ya están en .gitignore)
- ✅ Mantener solo 1-2 versiones más recientes para ejemplo
- ✅ Limpiar versiones antiguas

**Acción**:
```bash
# Script para mantener solo las 2 versiones más recientes
./scripts/clean-old-versions.sh
```

---

### 1️⃣2️⃣ data/01_raw/ Parcialmente Vacío (🟡 ATENCIÓN)
**Problema**: Solo tiene `shuttles.xlsx`, faltan otros archivos mencionados en catalog.yml

**catalog.yml menciona**:
- companies.csv ❌ FALTA
- reviews.csv ❌ FALTA
- shuttles.xlsx ✅ EXISTE

**Acción**:
- Verificar si estos archivos deberían existir
- Agregar archivos de ejemplo
- O actualizar catalog.yml y pipelines

---

## 📝 SCRIPT DE LIMPIEZA AUTOMATIZADO

### Crear scripts/clean-repo.sh

```bash
#!/bin/bash
set -e

echo "🧹 Limpiando archivos basura del repositorio..."
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Contador de acciones
CLEANED=0

# 1. Notebooks temporales
echo -e "${YELLOW}1. Eliminando notebooks temporales...${NC}"
if rm -f notebooks/Untitled.ipynb notebooks/Untitled1.ipynb 2>/dev/null; then
    echo -e "${GREEN}✓ Notebooks temporales eliminados${NC}"
    ((CLEANED++))
else
    echo -e "${GREEN}✓ No hay notebooks temporales${NC}"
fi

# 2. Directorio airflow_dags duplicado
echo -e "${YELLOW}2. Verificando directorio airflow_dags duplicado...${NC}"
if [ -d "airflow_dags" ]; then
    echo "   Encontrado directorio duplicado. ¿Eliminar? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        rm -rf airflow_dags/
        echo -e "${GREEN}✓ airflow_dags/ eliminado${NC}"
        ((CLEANED++))
    fi
else
    echo -e "${GREEN}✓ No existe directorio duplicado${NC}"
fi

# 3. Build artifacts
echo -e "${YELLOW}3. Eliminando build artifacts...${NC}"
rm -rf build/ dist/ src/spaceflights.egg-info/ 2>/dev/null
echo -e "${GREEN}✓ Build artifacts eliminados${NC}"
((CLEANED++))

# 4. info.log
echo -e "${YELLOW}4. Eliminando info.log...${NC}"
if rm -f info.log 2>/dev/null; then
    echo -e "${GREEN}✓ info.log eliminado${NC}"
    ((CLEANED++))
else
    echo -e "${GREEN}✓ info.log no existe${NC}"
fi

# 5. __pycache__ directories
echo -e "${YELLOW}5. Limpiando __pycache__ directories...${NC}"
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
echo -e "${GREEN}✓ __pycache__ directories eliminados${NC}"
((CLEANED++))

# 6. backups directory (con confirmación)
echo -e "${YELLOW}6. Verificando directorio backups/...${NC}"
if [ -d "backups" ] && [ "$(ls -A backups)" ]; then
    echo "   Directorio backups/ contiene archivos. ¿Eliminar? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        rm -rf backups/
        echo -e "${GREEN}✓ backups/ eliminado${NC}"
        ((CLEANED++))
    fi
else
    echo -e "${GREEN}✓ backups/ vacío o no existe${NC}"
fi

# 7. Limpiar logs antiguos (opcional)
echo -e "${YELLOW}7. ¿Limpiar logs antiguos? (y/N)${NC}"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    find logs/ -type f -name "*.log" -mtime +7 -delete 2>/dev/null || true
    echo -e "${GREEN}✓ Logs antiguos eliminados${NC}"
    ((CLEANED++))
fi

# 8. Verificar archivos en git que no deberían estar
echo -e "${YELLOW}8. Verificando archivos en git que deberían ser ignorados...${NC}"
if git rev-parse --git-dir > /dev/null 2>&1; then
    # Verificar uv.lock
    if git ls-files | grep -q "uv.lock"; then
        git rm --cached uv.lock 2>/dev/null || true
        echo -e "${YELLOW}   ! uv.lock removido de git (commit pendiente)${NC}"
    fi
    
    # Verificar docker-compose.override.yml
    if git ls-files | grep -q "docker-compose.override.yml"; then
        git rm --cached docker-compose.override.yml 2>/dev/null || true
        echo -e "${YELLOW}   ! docker-compose.override.yml removido de git (commit pendiente)${NC}"
    fi
    
    # Verificar build/
    if git ls-files | grep -q "^build/"; then
        git rm -r --cached build/ 2>/dev/null || true
        echo -e "${YELLOW}   ! build/ removido de git (commit pendiente)${NC}"
    fi
    
    # Verificar dist/
    if git ls-files | grep -q "^dist/"; then
        git rm -r --cached dist/ 2>/dev/null || true
        echo -e "${YELLOW}   ! dist/ removido de git (commit pendiente)${NC}"
    fi
fi

echo ""
echo -e "${GREEN}✅ Limpieza completada!${NC}"
echo "   Acciones realizadas: $CLEANED"
echo ""
echo -e "${YELLOW}📝 Próximos pasos:${NC}"
echo "   1. Revisar cambios: git status"
echo "   2. Si hay archivos removidos de git: git commit -m 'Clean up ignored files'"
echo "   3. Verificar .gitignore está actualizado"
```

---

## ✅ SCRIPT DE LIMPIEZA DE VERSIONES ANTIGUAS

### Crear scripts/clean-old-versions.sh

```bash
#!/bin/bash
set -e

echo "🗂️  Limpiando versiones antiguas de modelos y reportes..."
echo ""

KEEP_VERSIONS=2  # Mantener las 2 versiones más recientes

clean_versioned_dir() {
    local dir=$1
    local name=$(basename "$dir")
    
    if [ ! -d "$dir" ]; then
        return
    fi
    
    echo "Procesando: $name"
    
    # Contar versiones
    version_count=$(ls -1 "$dir" 2>/dev/null | wc -l)
    
    if [ "$version_count" -le "$KEEP_VERSIONS" ]; then
        echo "  ✓ Solo $version_count versiones, manteniendo todas"
        return
    fi
    
    # Eliminar versiones antiguas (mantener las más recientes)
    ls -1t "$dir" | tail -n +$((KEEP_VERSIONS + 1)) | while read -r version; do
        echo "  🗑️  Eliminando versión antigua: $version"
        rm -rf "$dir/$version"
    done
    
    echo "  ✓ Mantenidas $KEEP_VERSIONS versiones más recientes"
}

# Limpiar modelos
if [ -d "data/06_models" ]; then
    echo "📦 Limpiando modelos..."
    for model_dir in data/06_models/*/; do
        clean_versioned_dir "$model_dir"
    done
fi

# Limpiar reportes
if [ -d "data/08_reporting" ]; then
    echo "📊 Limpiando reportes..."
    for report_dir in data/08_reporting/*/; do
        clean_versioned_dir "$report_dir"
    done
fi

echo ""
echo "✅ Limpieza de versiones completada!"
echo ""
echo "Versiones actuales:"
du -sh data/06_models/*/ 2>/dev/null || true
du -sh data/08_reporting/*/ 2>/dev/null || true
```

---

## 🔍 VERIFICACIÓN POST-LIMPIEZA

### Checklist de Verificación

```bash
# 1. Verificar no hay archivos basura
echo "Verificando notebooks temporales..."
ls -la notebooks/Untitled* 2>/dev/null && echo "❌ AÚN EXISTEN" || echo "✅ OK"

echo "Verificando airflow_dags duplicado..."
[ -d "airflow_dags" ] && echo "❌ AÚN EXISTE" || echo "✅ OK"

echo "Verificando build artifacts..."
[ -d "build" ] && echo "❌ build/ AÚN EXISTE" || echo "✅ OK"
[ -d "dist" ] && echo "❌ dist/ AÚN EXISTE" || echo "✅ OK"

echo "Verificando info.log..."
[ -f "info.log" ] && echo "❌ AÚN EXISTE" || echo "✅ OK"

# 2. Verificar .gitignore actualizado
echo ""
echo "Verificando .gitignore..."
grep -q "build/" .gitignore && echo "✅ build/ en .gitignore" || echo "❌ FALTA build/"
grep -q "dist/" .gitignore && echo "✅ dist/ en .gitignore" || echo "❌ FALTA dist/"
grep -q "*.log" .gitignore && echo "✅ *.log en .gitignore" || echo "❌ FALTA *.log"

# 3. Verificar git status limpio
echo ""
echo "Git status:"
git status --short

# 4. Verificar tamaño del repo
echo ""
echo "Tamaño del directorio:"
du -sh .
```

---

## 📋 ACTUALIZAR .gitignore

### Asegurar que .gitignore tiene:

```gitignore
# Build artifacts
build/
dist/
*.egg-info/
*.egg

# Logs
*.log
logs/

# Temporary files
*.tmp
*.bak
*~

# Notebooks
.ipynb_checkpoints
notebooks/Untitled*.ipynb

# Python
__pycache__/
*.py[cod]
*$py.class

# Data
data/01_raw/
data/02_intermediate/
data/03_primary/
data/04_feature/
data/05_model_input/
data/06_models/
data/07_model_output/
data/08_reporting/

# Sessions
sessions/

# Backups
backups/

# Environment
.env

# UV
uv.lock

# Docker
docker-compose.override.yml
```

---

## 🎯 ORDEN DE EJECUCIÓN

### Paso a Paso:

```bash
# 1. Hacer backup del estado actual (por si acaso)
git status > pre-cleanup-status.txt
git diff > pre-cleanup-diff.txt

# 2. Ejecutar limpieza principal
chmod +x scripts/clean-repo.sh
./scripts/clean-repo.sh

# 3. Limpiar versiones antiguas (opcional)
chmod +x scripts/clean-old-versions.sh
./scripts/clean-old-versions.sh

# 4. Verificar estado
git status

# 5. Revisar cambios
git diff

# 6. Si todo OK, commit
git add .gitignore
git commit -m "chore: Clean up repository - remove build artifacts, temp files, and duplicates"

# 7. Si hay archivos removidos de git
git status | grep deleted && git commit -m "chore: Remove ignored files from git tracking"
```

---

## ⚠️ PRECAUCIONES

### Antes de Ejecutar Limpieza:

1. **Hacer backup** o trabajar en una rama
2. **Revisar backups/** antes de eliminar
3. **Verificar airflow_dags/** es idéntico a dags/
4. **Considerar** si necesitas versiones antiguas de modelos
5. **Probar** que el proyecto funciona después de limpieza

### Recuperación de Emergencia:

Si algo sale mal:
```bash
# Restaurar desde git
git checkout .
git clean -fd

# O usar backup
git stash
```

---

## 📊 RESULTADOS ESPERADOS

### Después de la limpieza:

- ✅ Sin notebooks temporales
- ✅ Sin directorios duplicados
- ✅ Sin build artifacts en git
- ✅ Sin logs commitados
- ✅ Solo 1-2 versiones de modelos para ejemplo
- ✅ .gitignore actualizado
- ✅ Repositorio más limpio y comprensible
- ✅ Menos confusión para estudiantes

### Beneficios:

1. **Claridad**: Estructura más clara y predecible
2. **Tamaño**: Repositorio más liviano
3. **Performance**: Clone y pull más rápidos
4. **Educación**: Sin archivos que distraigan o confundan
5. **Mantenibilidad**: Más fácil de mantener

---

## 📚 RESUMEN DE ARCHIVOS BASURA

| Archivo/Directorio | Acción | Prioridad | Razón |
|-------------------|--------|-----------|-------|
| notebooks/Untitled*.ipynb | ❌ Eliminar | 🔴 Crítica | Temporales sin valor |
| airflow_dags/ | ❌ Eliminar | 🔴 Crítica | Duplicado de dags/ |
| build/ | ❌ Eliminar | 🔴 Crítica | Build artifacts |
| dist/ | ❌ Eliminar | 🔴 Crítica | Distribution artifacts |
| src/*.egg-info/ | ❌ Eliminar | 🔴 Crítica | Installation artifacts |
| info.log | ❌ Eliminar | 🔴 Crítica | Log suelto |
| __pycache__/ | ❌ Limpiar | 🟡 Media | Archivos temporales |
| backups/ | ⚠️ Revisar | 🟡 Media | Puede tener datos útiles |
| logs/* (contenido) | ⚠️ Limpiar viejos | 🟢 Baja | Mantener estructura |
| data/06_models/* (versiones viejas) | ⚠️ Limpiar | 🟢 Baja | Mantener 1-2 recientes |
| data/08_reporting/* (versiones viejas) | ⚠️ Limpiar | 🟢 Baja | Mantener 1-2 recientes |

---

**Última actualización**: 2025-10-09
**Versión**: 1.0
**Estado**: Listo para ejecutar

