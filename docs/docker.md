# 🐳 Docker Guide - Spaceflights

## Docker Architecture

The project uses a multi-service Docker Compose setup with different profiles for various use cases.

## Docker Compose Files

### Main Files

1. **docker-compose.yml**
   - Main compose file with all services
   - Uses profiles for service selection
   - Base configuration

2. **docker-compose.airflow.yml**
   - Separate compose for Airflow
   - Includes Airflow webserver, scheduler, and dependencies
   - Independent from main compose

3. **docker-compose.override.yml.example**
   - Template for local customization
   - Copy to `docker-compose.override.yml` to use
   - Automatically loaded when present
   - Gitignored

## Dockerfiles

Located in `docker/` directory:

- **Dockerfile.kedro**: Base Kedro service
- **Dockerfile.jupyter**: JupyterLab environment
- **Dockerfile.airflow**: Airflow with Kedro integration

## Services

### Development Profile

```bash
docker-compose --profile development up -d
```

**Services**:
- `jupyter-lab`: JupyterLab on port 8888
- `kedro-viz`: Kedro Viz on port 4141

### Production Profile

```bash
docker-compose --profile production up -d
```

**Services**:
- `kedro-prod`: Automated pipeline execution
- `kedro-scheduler`: Scheduled execution every hour
- `kedro-viz`: Pipeline visualization

### Database Profile

```bash
docker-compose --profile database up -d
```

**Services**:
- `postgres`: PostgreSQL on port 5433

### Cache Profile

```bash
docker-compose --profile cache up -d
```

**Services**:
- `redis`: Redis on port 6379

## Networking

All services connect through `spaceflights-network` bridge network.

```bash
# View network
docker network ls | grep spaceflights

# Inspect network
docker network inspect spaceflights-network
```

## Volumes

### Bind Mounts (Code Sync)

```yaml
volumes:
  - ./src:/app/src       # Source code
  - ./conf:/app/conf     # Configuration
  - ./data:/app/data     # Data
  - ./logs:/app/logs     # Logs
  - ./notebooks:/app/notebooks  # Notebooks
```

### Named Volumes (Persistence)

```yaml
volumes:
  postgres_data:   # PostgreSQL data
  redis_data:      # Redis data
  prometheus_data: # Prometheus data (if using monitoring)
```

## Common Commands

### Build

```bash
# Build all images
docker-compose build

# Build specific service
docker-compose build jupyter-lab

# Build without cache
docker-compose build --no-cache
```

### Start/Stop

```bash
# Start services
docker-compose --profile development up -d

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Logs

```bash
# All logs
docker-compose logs -f

# Specific service
docker-compose logs -f jupyter-lab

# Last 100 lines
docker-compose logs --tail=100 kedro-viz
```

### Execute Commands

```bash
# Interactive shell
docker-compose exec jupyter-lab bash

# Run Kedro command
docker-compose exec jupyter-lab kedro run

# Run tests
docker-compose exec jupyter-lab pytest

# Check Kedro info
docker-compose exec jupyter-lab kedro info
```

## Custom Override

### When to Use

Use `docker-compose.override.yml` when you need:
- Custom environment variables
- Different ports
- Additional volumes
- Modified commands
- Development-specific settings

### How to Use

```bash
# 1. Copy template
cp docker-compose.override.yml.example docker-compose.override.yml

# 2. Edit file
nano docker-compose.override.yml

# 3. Start services (override loaded automatically)
docker-compose up -d
```

### Example Overrides

#### Change Jupyter Port

```yaml
services:
  jupyter-lab:
    ports:
      - "9999:8888"  # Use port 9999 instead of 8888
```

#### Add Debug Port

```yaml
services:
  jupyter-lab:
    ports:
      - "8888:8888"
      - "5678:5678"  # Python debugger port
```

#### Mount Additional Directory

```yaml
services:
  jupyter-lab:
    volumes:
      - ./src:/app/src
      - ./my-data:/app/my-data  # Additional mount
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port
lsof -i :8888

# Change port in docker-compose.override.yml
services:
  jupyter-lab:
    ports:
      - "9999:8888"
```

### Permission Issues

```bash
# Fix permissions
sudo chown -R $USER:$USER data/ logs/ sessions/
```

### Out of Disk Space

```bash
# Clean up
docker system prune -a

# Remove unused volumes
docker volume prune
```

### Container Won't Start

```bash
# View logs
docker-compose logs <service-name>

# Rebuild without cache
docker-compose build --no-cache <service-name>

# Reset everything
docker-compose down -v
docker system prune -a
docker-compose up -d
```

## Best Practices

1. **Use profiles** for environment separation
2. **Use .env** for sensitive data
3. **Use override.yml** for local customization
4. **Don't commit** docker-compose.override.yml
5. **Use named volumes** for data persistence
6. **Use bind mounts** for code sync
7. **Tag images** with versions
8. **Use healthchecks** for service readiness

## Advanced

### Multi-stage Builds

Dockerfiles use multi-stage builds for optimization:

```dockerfile
# Build stage
FROM python:3.11 as builder
RUN pip install --user <packages>

# Runtime stage
FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
```

### Resource Limits

Add to docker-compose.override.yml:

```yaml
services:
  jupyter-lab:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
```

### Health Checks

Services include health checks:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:4141"]
  interval: 30s
  timeout: 10s
  retries: 3
```

## See Also

- [Setup Guide](./setup.md)
- [Airflow Guide](./airflow.md)
- [Troubleshooting](./troubleshooting.md)

