# 🔧 Troubleshooting Guide

## Common Issues and Solutions

### Docker Issues

#### 1. Docker Network Not Found

**Error**:
```
Error: network spaceflights-network declared as external, but could not be found
```

**Solution**:
```bash
docker network create spaceflights-network
```

#### 2. Port Already in Use

**Error**:
```
Error: bind: address already in use
```

**Solution**:
```bash
# Find process using the port
lsof -i :8888

# Kill process or change port in docker-compose.override.yml
services:
  jupyter-lab:
    ports:
      - "9999:8888"  # Use different port
```

#### 3. Permission Denied

**Error**:
```
Permission denied: './data'
```

**Solution**:
```bash
# Fix permissions
sudo chown -R $USER:$USER data/ logs/ sessions/

# Or
chmod -R 755 data/ logs/ sessions/
```

#### 4. Container Won't Start

**Solution**:
```bash
# View logs
docker-compose logs <service-name>

# Rebuild without cache
docker-compose build --no-cache <service-name>

# Complete reset
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Kedro Issues

#### 1. Module Not Found

**Error**:
```
ModuleNotFoundError: No module named 'spaceflights'
```

**Solution**:
```bash
# Inside container
docker-compose exec jupyter-lab pip install -e .

# Or rebuild image
docker-compose build jupyter-lab
```

#### 2. Pipeline Not Found

**Error**:
```
Pipeline 'xyz' not found
```

**Solution**:
```bash
# List available pipelines
docker-compose exec jupyter-lab kedro registry list

# Check pipeline_registry.py
cat src/spaceflights/pipeline_registry.py
```

#### 3. Dataset Not Found in Catalog

**Error**:
```
DataSetError: 'xyz' not found in DataCatalog
```

**Solution**:
```bash
# Check catalog
cat conf/base/catalog.yml

# List catalog entries
docker-compose exec jupyter-lab kedro catalog list
```

### Airflow Issues

#### 1. DAGs Not Appearing

**Solution**:
```bash
# Check DAGs folder is mounted
docker-compose -f docker-compose.airflow.yml exec airflow-webserver ls /opt/airflow/dags

# Check DAG syntax
docker-compose -f docker-compose.airflow.yml exec airflow-webserver python /opt/airflow/dags/spaceflights_dag.py

# Trigger DAG scan
docker-compose -f docker-compose.airflow.yml restart airflow-scheduler
```

#### 2. Airflow Login Issues

**Default credentials**:
- Username: `admin`
- Password: `admin`

**If not working**:
```bash
# Recreate admin user
docker-compose -f docker-compose.airflow.yml exec airflow-webserver \
  airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin
```

#### 3. Airflow Database Locked

**Solution**:
```bash
# Reset Airflow database
docker-compose -f docker-compose.airflow.yml down -v
docker-compose -f docker-compose.airflow.yml up -d
```

### Data Issues

#### 1. Data Not Persisting

**Solution**:
```bash
# Check volumes
docker volume ls | grep spaceflights

# Inspect volume
docker volume inspect <volume-name>

# Verify mount in container
docker-compose exec jupyter-lab ls -la /app/data
```

#### 2. Out of Disk Space

**Solution**:
```bash
# Check disk usage
docker system df

# Clean up
docker system prune -a
docker volume prune

# Keep only recent data versions
# (Manual cleanup of data/06_models/ and data/08_reporting/)
```

### Performance Issues

#### 1. Slow Pipeline Execution

**Solutions**:
- Increase Docker resources (CPU/Memory)
- Use `--parallel` flag if supported
- Profile code to find bottlenecks
- Optimize data processing steps

#### 2. Out of Memory

**Solution**:
```bash
# Increase Docker memory limit
# Docker Desktop → Preferences → Resources → Memory

# Or add limits in docker-compose.override.yml
services:
  jupyter-lab:
    deploy:
      resources:
        limits:
          memory: 8G
```

### Jupyter Issues

#### 1. JupyterLab Not Accessible

**Solution**:
```bash
# Check service is running
docker-compose ps jupyter-lab

# Check logs
docker-compose logs jupyter-lab

# Get access URL with token
docker-compose logs jupyter-lab | grep "http://127"
```

#### 2. Kernel Not Found

**Solution**:
```bash
# Inside JupyterLab terminal or container
pip install ipykernel
python -m ipykernel install --user --name=spaceflights
```

### Network Issues

#### 1. Services Can't Communicate

**Solution**:
```bash
# Verify all services are on same network
docker network inspect spaceflights-network

# Restart with network recreation
docker-compose down
docker network rm spaceflights-network
docker network create spaceflights-network
docker-compose up -d
```

#### 2. Can't Access Services from Host

**Solution**:
```bash
# Check port mappings
docker-compose ps

# Verify firewall allows connections
# macOS: System Preferences → Security → Firewall
# Linux: sudo ufw status
```

## Debug Mode

### Enable Debug Logging

**In docker-compose.override.yml**:
```yaml
services:
  jupyter-lab:
    environment:
      - KEDRO_LOGGING_LEVEL=DEBUG
```

**In code**:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Access Container Shell

```bash
# Interactive shell
docker-compose exec jupyter-lab bash

# Or
docker-compose exec jupyter-lab /bin/sh
```

### Inspect Running Process

```bash
# Inside container
ps aux | grep python
top
df -h
```

## Getting Help

### Check Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f jupyter-lab

# Last N lines
docker-compose logs --tail=100 jupyter-lab
```

### Verify Configuration

```bash
# Check docker-compose configuration
docker-compose config

# Check Kedro configuration
docker-compose exec jupyter-lab kedro info
```

### Health Checks

```bash
# Check service health
docker-compose ps

# Inspect container
docker inspect <container-id>
```

## Still Having Issues?

1. Check [Setup Guide](./setup.md) for correct installation
2. Review [Docker Guide](./docker.md) for Docker-specific issues
3. Check [Architecture](../ARCHITECTURE.md) for system understanding
4. Search existing issues on GitHub
5. Create new issue with:
   - Error message
   - Steps to reproduce
   - docker-compose logs output
   - System information (OS, Docker version)

## Useful Commands

```bash
# Complete cleanup and restart
docker-compose down -v
docker system prune -a
docker volume prune
docker network create spaceflights-network
./start.sh development

# Check system resources
docker stats

# View all containers (including stopped)
docker ps -a

# Remove all stopped containers
docker container prune

# View Docker disk usage
docker system df -v
```

