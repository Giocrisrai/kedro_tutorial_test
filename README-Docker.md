# 🚀 Spaceflights - Docker Setup

Este proyecto Kedro está configurado para ejecutarse en Docker y Docker Compose, proporcionando un entorno de desarrollo y producción consistente.

## 📋 Servicios Disponibles

### 🔧 Servicios Principales
- **kedro-app**: Servicio principal de Kedro para ejecutar pipelines
- **jupyter-lab**: Entorno de desarrollo interactivo con JupyterLab
- **kedro-viz**: Visualización de pipelines y metadatos

### 🗄️ Servicios de Datos (Opcionales)
- **postgres**: Base de datos PostgreSQL para datos estructurados
- **redis**: Cache y gestión de sesiones

### 📊 Servicios de Monitoreo (Opcionales)
- **prometheus**: Métricas y monitoreo del sistema

## 🚀 Inicio Rápido

### 1. Configuración Inicial
```bash
# Copiar archivo de configuración de entorno
cp env.example .env

# Editar variables de entorno según tu configuración
nano .env
```

### 2. Construir las Imágenes
```bash
# Construir todas las imágenes
docker-compose build

# O construir una imagen específica
docker-compose build kedro-app
```

### 3. Ejecutar Servicios

#### Desarrollo Completo
```bash
# Levantar todos los servicios de desarrollo
docker-compose --profile development up -d

# Ver logs
docker-compose logs -f
```

#### Solo JupyterLab
```bash
# Solo JupyterLab para desarrollo interactivo
docker-compose --profile development up jupyter-lab -d
```

#### Solo Kedro Viz
```bash
# Solo visualización de pipelines
docker-compose --profile development up kedro-viz -d
```

#### Con Base de Datos
```bash
# Incluir PostgreSQL y Redis
docker-compose --profile development --profile database --profile cache up -d
```

## 🎯 Comandos Útiles

### Ejecutar Pipelines
```bash
# Pipeline completo
./scripts/run-pipeline.sh

# Pipeline específico
./scripts/run-pipeline.sh data_processing
./scripts/run-pipeline.sh data_science
./scripts/run-pipeline.sh reporting

# Con opciones adicionales
./scripts/run-pipeline.sh data_processing --parallel
```

### Acceso a Contenedores
```bash
# Acceso interactivo al contenedor principal
docker-compose exec kedro-app bash

# Ejecutar comandos específicos
docker-compose exec kedro-app kedro info
docker-compose exec kedro-app kedro catalog list
```

### Gestión de Datos
```bash
# Inicializar datos de ejemplo
docker-compose exec kedro-app /app/scripts/init-data.sh

# Ver estado de los datos
docker-compose exec kedro-app kedro catalog list
```

## 🌐 Acceso a Servicios

| Servicio | URL | Descripción |
|----------|-----|-------------|
| JupyterLab | http://localhost:8888 | Entorno de desarrollo interactivo |
| Kedro Viz | http://localhost:4141 | Visualización de pipelines |
| PostgreSQL | localhost:5432 | Base de datos (si está habilitada) |
| Redis | localhost:6379 | Cache (si está habilitado) |
| Prometheus | http://localhost:9090 | Métricas (si está habilitado) |

## 🔧 Configuración Avanzada

### Variables de Entorno
Edita el archivo `.env` para personalizar:
- Configuración de Kedro
- Credenciales de base de datos
- Tokens de Jupyter
- Configuración de logging

### Perfiles de Docker Compose
- `development`: Servicios de desarrollo (Jupyter, Kedro Viz)
- `production`: Solo servicios de producción
- `database`: Base de datos PostgreSQL
- `cache`: Redis para cache
- `monitoring`: Prometheus para métricas

### Volúmenes Persistentes
Los siguientes directorios se mantienen entre reinicios:
- `./data/`: Datos del proyecto
- `./logs/`: Logs de ejecución
- `./sessions/`: Sesiones de Kedro
- `postgres_data`: Datos de PostgreSQL
- `redis_data`: Datos de Redis

## 🐛 Solución de Problemas

### Problemas Comunes

1. **Puerto ya en uso**
   ```bash
   # Verificar qué proceso usa el puerto
   lsof -i :8888
   
   # Cambiar puerto en docker-compose.override.yml
   ```

2. **Permisos de archivos**
   ```bash
   # Ajustar permisos
   sudo chown -R $USER:$USER data/ logs/ sessions/
   ```

3. **Contenedor no inicia**
   ```bash
   # Ver logs detallados
   docker-compose logs kedro-app
   
   # Reconstruir imagen
   docker-compose build --no-cache kedro-app
   ```

4. **Problemas de memoria**
   ```bash
   # Limpiar contenedores no utilizados
   docker system prune -a
   
   # Ver uso de espacio
   docker system df
   ```

### Comandos de Limpieza
```bash
# Detener todos los servicios
docker-compose down

# Eliminar volúmenes (¡CUIDADO! Elimina datos)
docker-compose down -v

# Limpiar imágenes no utilizadas
docker image prune -a
```

## 📚 Recursos Adicionales

- [Documentación de Kedro](https://docs.kedro.org/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [JupyterLab Documentation](https://jupyterlab.readthedocs.io/)

## 🤝 Contribución

Para contribuir al proyecto:
1. Fork el repositorio
2. Crea una rama para tu feature
3. Haz commit de tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo LICENSE para más detalles.
