# 🚀 GitHub Actions CI/CD Pipeline

## 📋 Overview

Este proyecto incluye un sistema completo de CI/CD usando GitHub Actions que garantiza la calidad del código y la funcionalidad del sistema antes de cualquier merge a la rama principal.

## 🔧 Workflows Configurados

### 1. **CI Pipeline** (`.github/workflows/ci.yml`)
Se ejecuta en cada push y pull request a las ramas `main` y `develop`.

#### Jobs incluidos:
- **🔍 Linting & Code Quality**: Verificación de código con ruff y mypy
- **🧪 Unit Tests**: Pruebas unitarias con cobertura de código
- **🔗 Integration Tests**: Pruebas de integración de pipelines
- **⚙️ Functional Tests**: Validación de DAGs de Airflow
- **🐳 Docker Tests**: Construcción y pruebas de contenedores
- **🎯 End-to-End Tests**: Pruebas completas del sistema
- **🔒 Security Scan**: Escaneo de seguridad con safety y bandit
- **✅ Final Validation**: Validación final y reporte de resultados

### 2. **Deployment Pipeline** (`.github/workflows/deploy.yml`)
Se ejecuta en push a `main` o creación de tags de versión.

#### Funcionalidades:
- **🐳 Build & Push Docker Images**: Construcción y push de imágenes a GitHub Container Registry
- **🚀 Deploy to Staging**: Despliegue automático a ambiente de staging
- **🚀 Deploy to Production**: Despliegue automático a producción
- **📦 Create Release**: Creación automática de releases de GitHub

### 3. **PR Checks** (`.github/workflows/pr-checks.yml`)
Se ejecuta en cada pull request para validación rápida.

#### Validaciones:
- **🔍 PR Validation**: Linting, formatting y type checking
- **⚡ Quick Tests**: Pruebas unitarias rápidas
- **🐳 Docker Build Test**: Construcción de contenedores
- **📋 PR Summary**: Resumen automático de validaciones

## 🛡️ Protección de Ramas

### Rama `main`
- ✅ **Required Status Checks**: Todos los tests deben pasar
- ✅ **Required Reviews**: Mínimo 1 aprobación requerida
- ✅ **Dismiss Stale Reviews**: Reviews obsoletos se descartan
- ✅ **Require Conversation Resolution**: Conversaciones deben resolverse
- ✅ **Restrict Pushes**: Solo pushes via PR permitidos
- ✅ **Force Push Protection**: Force pushes bloqueados

### Rama `develop`
- ✅ **Required Status Checks**: Tests básicos requeridos
- ✅ **Required Reviews**: 1 aprobación requerida
- ✅ **Allow Force Pushes**: Force pushes permitidos para desarrollo

## 🚀 Cómo Usar

### Para Desarrolladores

#### 1. **Crear una nueva feature**
```bash
# Crear nueva rama
git checkout -b feature/nueva-funcionalidad

# Hacer cambios
# ... código ...

# Commit y push
git add .
git commit -m "feat: agregar nueva funcionalidad"
git push origin feature/nueva-funcionalidad
```

#### 2. **Crear Pull Request**
- Ir a GitHub y crear PR
- El workflow de PR Checks se ejecutará automáticamente
- Revisar el resumen generado automáticamente
- Esperar aprobaciones si es requerido

#### 3. **Merge a main**
- Una vez que todos los checks pasen y tengas aprobaciones
- Hacer merge a main
- El CI Pipeline completo se ejecutará
- Si todo pasa, se desplegará automáticamente

### Para Administradores

#### 1. **Configurar Protecciones de Rama**
```bash
# Ejecutar script de configuración
./scripts/setup-github-protections.sh
```

#### 2. **Configurar Secrets**
Ver `scripts/setup-secrets.md` para configurar secrets requeridos.

#### 3. **Monitorear Deployments**
- Revisar logs de GitHub Actions
- Verificar deployments en ambientes de staging/producción
- Monitorear métricas y alertas

## 📊 Métricas y Monitoreo

### Cobertura de Código
- **Objetivo**: >80% de cobertura
- **Reporte**: Generado automáticamente en cada run
- **Visualización**: Disponible en GitHub Actions logs

### Tiempo de Ejecución
- **PR Checks**: ~5-10 minutos
- **CI Pipeline**: ~15-20 minutos
- **Deployment**: ~10-15 minutos

### Notificaciones
- **Slack/Teams**: Configurables via webhooks
- **Email**: Notificaciones automáticas de GitHub
- **GitHub**: Status checks visibles en PRs

## 🔧 Configuración Avanzada

### Variables de Entorno
```yaml
env:
  PYTHON_VERSION: '3.11'
  KEDRO_ENV: 'base'
  REGISTRY: ghcr.io
```

### Secrets Requeridos
- `GITHUB_TOKEN`: Automático
- `DOCKER_USERNAME`: Para push de imágenes
- `DOCKER_PASSWORD`: Para push de imágenes
- `AWS_ACCESS_KEY_ID`: Para deployment a AWS
- `AWS_SECRET_ACCESS_KEY`: Para deployment a AWS

### Matrices de Testing
```yaml
strategy:
  matrix:
    python-version: [3.10, 3.11, 3.12]
    os: [ubuntu-latest, windows-latest, macos-latest]
```

## 🐛 Troubleshooting

### Problemas Comunes

#### 1. **Tests Fallando**
```bash
# Ejecutar tests localmente
python scripts/run_tests.py --type all

# Verificar logs específicos
python -m pytest tests/ -v --tb=long
```

#### 2. **Docker Build Fallando**
```bash
# Construir localmente
docker build -f docker/Dockerfile.kedro -t test .

# Verificar logs
docker build -f docker/Dockerfile.kedro -t test . --progress=plain
```

#### 3. **Deployment Fallando**
- Verificar secrets configurados
- Revisar permisos de deployment
- Verificar conectividad con servicios externos

### Logs y Debugging
- **GitHub Actions Logs**: Disponibles en la pestaña "Actions"
- **Artifacts**: Reportes y logs descargables
- **Real-time Logs**: Disponibles durante la ejecución

## 📈 Mejoras Futuras

### Funcionalidades Planificadas
- [ ] **Matrix Testing**: Testing en múltiples versiones de Python
- [ ] **Parallel Jobs**: Ejecución paralela de tests para velocidad
- [ ] **Caching**: Cache de dependencias para builds más rápidos
- [ ] **Slack Integration**: Notificaciones automáticas a Slack
- [ ] **Performance Testing**: Tests de rendimiento automatizados
- [ ] **Security Scanning**: Escaneo avanzado de vulnerabilidades

### Optimizaciones
- [ ] **Build Optimization**: Optimización de tiempos de build
- [ ] **Resource Management**: Gestión eficiente de recursos
- [ ] **Cost Optimization**: Optimización de costos de CI/CD

## 📚 Recursos Adicionales

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Kedro Documentation](https://docs.kedro.org/)
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Docker Documentation](https://docs.docker.com/)

## 🤝 Contribuir

Para contribuir al sistema de CI/CD:

1. **Fork** el repositorio
2. **Crear** una nueva rama
3. **Hacer** cambios en los workflows
4. **Probar** localmente
5. **Crear** un Pull Request
6. **Esperar** aprobaciones y merge

---

**¡El sistema de CI/CD está diseñado para garantizar la calidad y confiabilidad del proyecto Spaceflights! 🚀**
