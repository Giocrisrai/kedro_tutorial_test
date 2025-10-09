# ⚡ QUICK FIXES - Soluciones Rápidas

## 🚨 Problemas Críticos y Sus Soluciones

---

## 1️⃣ FIX: Docker Network Not Found

### Problema
```
Error: network spaceflights-network declared as external, but could not be found
```

### Solución Inmediata
```bash
docker network create spaceflights-network
```

### Solución Permanente
Editar `docker-compose.airflow.yml` línea 155-156:

**Cambiar:**
```yaml
networks:
  spaceflights-network:
    external: true
```

**Por:**
```yaml
networks:
  spaceflights-network:
    name: spaceflights-network
    driver: bridge
```

O simplemente:
```yaml
networks:
  spaceflights-network:
```

---

## 2️⃣ FIX: Generar Nuevo Fernet Key

### Problema
Fernet key hardcodeada en `docker-compose.airflow.yml`

### Solución

**1. Generar nueva key:**
```bash
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

**2. Agregar a `.env`:**
```bash
echo "AIRFLOW_FERNET_KEY=<tu-key-generada>" >> .env
```

**3. Actualizar docker-compose.airflow.yml:**

**Cambiar:**
```yaml
- AIRFLOW__CORE__FERNET_KEY=M0Q5RhSDhhTEZwd5bShf0hILBvTMz2q3-vdDvkiHxOE=
```

**Por:**
```yaml
- AIRFLOW__CORE__FERNET_KEY=${AIRFLOW_FERNET_KEY}
```

---

## 3️⃣ FIX: Eliminar Notebooks Temporales

### Problema
Notebooks sin nombre en el repositorio

### Solución
```bash
cd /Users/giocrisraigodoy/Documents/DUOC/Semestre_2025_2/Machine\ Learning/spaceflights
rm -f notebooks/Untitled.ipynb notebooks/Untitled1.ipynb
```

---

## 4️⃣ FIX: Actualizar Fechas en DAGs

### Problema
`start_date=datetime(2023,1,1)` desactualizado

### Solución

**Editar `dags/spaceflights_dag.py` línea 52:**

**Cambiar:**
```python
start_date=datetime(2023,1,1),
```

**Por:**
```python
from airflow.utils.dates import days_ago
# ... más abajo
start_date=days_ago(1),
```

**O:**
```python
start_date=datetime(2025,10,1),
```

---

## 5️⃣ FIX: Crear .dockerignore

### Problema
No existe `.dockerignore`, lo que hace que las imágenes sean muy grandes

### Solución

**Crear `.dockerignore`:**
```bash
cat > .dockerignore << 'EOF'
# Git
.git
.gitignore

# Python
__pycache__
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

# Data
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

# Documentation
*.md
docs/

# Tests
tests/
.pytest_cache/
.coverage
htmlcov/

# Notebooks
notebooks/.ipynb_checkpoints
notebooks/Untitled*.ipynb

# OS
.DS_Store
._*
EOF
```

---

## 6️⃣ FIX: Mover Credenciales a .env

### Problema
Credenciales hardcodeadas en docker-compose.yml

### Solución

**1. Actualizar `.env`:**
```bash
# Agregar al final de .env
POSTGRES_DB=spaceflights
POSTGRES_USER=kedro
POSTGRES_PASSWORD=secure-password-$(openssl rand -hex 8)
AIRFLOW_POSTGRES_USER=airflow
AIRFLOW_POSTGRES_PASSWORD=secure-password-$(openssl rand -hex 8)
AIRFLOW_POSTGRES_DB=airflow
```

**2. Actualizar docker-compose.yml:**

**En servicio postgres (línea 138-141):**
```yaml
environment:
  - POSTGRES_DB=${POSTGRES_DB}
  - POSTGRES_USER=${POSTGRES_USER}
  - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
```

**3. Actualizar docker-compose.airflow.yml:**

**En servicio airflow-postgres (línea 11-14):**
```yaml
environment:
  - POSTGRES_USER=${AIRFLOW_POSTGRES_USER}
  - POSTGRES_PASSWORD=${AIRFLOW_POSTGRES_PASSWORD}
  - POSTGRES_DB=${AIRFLOW_POSTGRES_DB}
```

---

## 7️⃣ FIX: Validar Health Checks

### Problema
Health check de kedro-viz puede fallar si curl no está instalado

### Solución

**Editar `docker/Dockerfile.kedro` agregar curl:**

**Después de la línea 22 (instalación de dependencias):**
```dockerfile
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*
```

---

## 8️⃣ FIX: Configurar PYTHONPATH Consistentemente

### Problema
PYTHONPATH puede no estar configurado correctamente en todos los servicios

### Solución

**Verificar en TODOS los servicios en docker-compose.yml y docker-compose.airflow.yml:**

```yaml
environment:
  - PYTHONPATH=/app/src
```

**Servicios a verificar:**
- kedro-prod
- kedro-scheduler
- jupyter-lab
- kedro-viz
- airflow-init
- airflow-webserver
- airflow-scheduler

---

## 9️⃣ FIX: Actualizar env.example

### Problema
`env.example` no tiene todas las variables necesarias

### Solución

**Actualizar `env.example`:**
```bash
cat > env.example << 'EOF'
# Archivo de ejemplo para variables de entorno
# Copia este archivo como .env y ajusta los valores

# Configuración de Kedro
KEDRO_ENV=local
KEDRO_LOGGING_LEVEL=INFO
KEDRO_HOME=/app
KEDRO_CONFIG_FILE=conf/base/parameters.yml

# Configuración de Jupyter
JUPYTER_TOKEN=
JUPYTER_ALLOW_INSECURE_WRITES=true

# Configuración de Base de Datos PostgreSQL (Kedro)
POSTGRES_DB=spaceflights
POSTGRES_USER=kedro
POSTGRES_PASSWORD=change-me-to-secure-password
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Configuración de Base de Datos PostgreSQL (Airflow)
AIRFLOW_POSTGRES_DB=airflow
AIRFLOW_POSTGRES_USER=airflow
AIRFLOW_POSTGRES_PASSWORD=change-me-to-secure-password

# Configuración de Airflow
AIRFLOW_FERNET_KEY=generate-with-python-script
# Para generar: python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Configuración de Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=

# Configuración de Kedro Viz
KEDRO_VIZ_HOST=0.0.0.0
KEDRO_VIZ_PORT=4141

# Configuración de Monitoreo
PROMETHEUS_PORT=9090

# Configuración de Desarrollo
PYTHONPATH=/app/src
DEBUG=true
EOF
```

---

## 🔟 FIX: Verificar Permisos de Archivos

### Problema
Problemas de permisos al ejecutar dentro de contenedores

### Solución

**Si tienes problemas de permisos:**
```bash
# En el host (tu máquina)
sudo chown -R $USER:$USER data/ logs/ sessions/
chmod -R 755 data/ logs/ sessions/

# O si quieres usar el mismo UID del contenedor
docker-compose exec jupyter-lab id
# Nota el UID, luego:
sudo chown -R <UID>:<UID> data/ logs/ sessions/
```

---

## 🛠️ SCRIPT DE FIX AUTOMÁTICO

### Crear y Ejecutar

**1. Crear `scripts/quick-fix.sh`:**
```bash
#!/bin/bash
set -e

echo "🔧 Aplicando Quick Fixes..."

# Fix 1: Crear network
echo "1️⃣ Creando Docker network..."
docker network create spaceflights-network 2>/dev/null || echo "Network ya existe ✓"

# Fix 2: Eliminar notebooks temporales
echo "2️⃣ Eliminando notebooks temporales..."
rm -f notebooks/Untitled.ipynb notebooks/Untitled1.ipynb 2>/dev/null || true
echo "✓ Notebooks limpiados"

# Fix 3: Crear .dockerignore si no existe
if [ ! -f .dockerignore ]; then
    echo "3️⃣ Creando .dockerignore..."
    cat > .dockerignore << 'DOCKERIGNORE'
.git
.gitignore
__pycache__
*.py[cod]
.env
.venv
venv/
data/
logs/
sessions/
*.log
backups/
.vscode/
.idea/
*.md
docs/
tests/
.pytest_cache/
notebooks/.ipynb_checkpoints
.DS_Store
DOCKERIGNORE
    echo "✓ .dockerignore creado"
else
    echo "3️⃣ .dockerignore ya existe ✓"
fi

# Fix 4: Verificar .env existe
if [ ! -f .env ]; then
    echo "4️⃣ Creando .env desde template..."
    cp env.example .env
    echo "⚠️  IMPORTANTE: Edita .env y configura credenciales seguras"
else
    echo "4️⃣ .env ya existe ✓"
fi

# Fix 5: Ajustar permisos
echo "5️⃣ Ajustando permisos de directorios..."
chmod +x scripts/*.sh 2>/dev/null || true
mkdir -p data logs sessions
chmod -R 755 data logs sessions
echo "✓ Permisos ajustados"

echo ""
echo "✅ Quick Fixes aplicados!"
echo ""
echo "⚠️  ACCIONES MANUALES REQUERIDAS:"
echo "1. Generar Fernet Key y agregar a .env:"
echo "   python3 -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\""
echo ""
echo "2. Editar .env y configurar contraseñas seguras"
echo ""
echo "3. Actualizar docker-compose.airflow.yml (línea 155-156):"
echo "   Cambiar 'external: true' por solo 'spaceflights-network:'"
echo ""
echo "4. Actualizar fechas en DAGs de Airflow (start_date)"
echo ""
echo "🚀 Próximo paso: ./start.sh development"
```

**2. Hacer ejecutable:**
```bash
chmod +x scripts/quick-fix.sh
```

**3. Ejecutar:**
```bash
./scripts/quick-fix.sh
```

---

## ✅ VALIDACIÓN POST-FIXES

### Verificar que todo funciona:

```bash
# 1. Verificar network existe
docker network ls | grep spaceflights-network

# 2. Verificar .env existe
ls -la .env

# 3. Verificar .dockerignore existe
ls -la .dockerignore

# 4. Verificar permisos
ls -ld data/ logs/ sessions/

# 5. Test build
docker-compose build jupyter-lab

# 6. Test startup
./start.sh development

# 7. Verificar servicios
docker-compose ps

# 8. Test pipeline
docker-compose exec jupyter-lab kedro run --pipeline data_processing
```

---

## 🆘 SI ALGO FALLA

### Logs y Debugging

```bash
# Ver logs de servicios
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs jupyter-lab

# Verificar configuración
docker-compose config

# Rebuild completo
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d

# Acceso a shell para debugging
docker-compose exec jupyter-lab bash
```

### Reset Completo

```bash
# ⚠️ CUIDADO: Esto elimina TODOS los datos
docker-compose down -v
docker system prune -a --volumes
rm -rf data/* logs/* sessions/*
./start.sh development
```

---

## 📞 PROBLEMAS COMUNES

### "Cannot connect to Docker daemon"
```bash
# Iniciar Docker Desktop
open -a Docker  # macOS
# o
sudo systemctl start docker  # Linux
```

### "Port already in use"
```bash
# Encontrar proceso usando el puerto
lsof -i :8888  # o el puerto que está ocupado

# Matar proceso
kill -9 <PID>

# O cambiar puerto en docker-compose.override.yml
```

### "Permission denied"
```bash
# Agregar usuario a grupo docker (Linux)
sudo usermod -aG docker $USER
newgrp docker
```

### "Out of memory"
```bash
# Aumentar memoria en Docker Desktop
# Docker Desktop → Preferences → Resources → Memory

# O limpiar espacio
docker system prune -a
```

---

## ✨ RESULTADO ESPERADO

Después de aplicar todos los quick fixes, deberías poder:

1. ✅ Ejecutar `./start.sh development` sin errores
2. ✅ Acceder a JupyterLab en http://localhost:8888
3. ✅ Acceder a Kedro Viz en http://localhost:4141
4. ✅ Ejecutar pipelines sin errores
5. ✅ Iniciar Airflow con `./start.sh airflow`
6. ✅ Ver DAGs en Airflow UI

---

**Tiempo total estimado**: 15-30 minutos
**Dificultad**: Baja a Media
**Requisitos**: Docker Desktop, bash, Python 3.9+

