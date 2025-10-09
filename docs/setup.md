# 🚀 Setup Guide - Spaceflights

## Prerequisites

- **Docker Desktop** (20.10+)
- **Docker Compose** (2.0+)
- **Python 3.11+** (optional, for local development)
- **Git**

## Quick Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd spaceflights
```

### 2. Environment Configuration

```bash
# Copy environment template
cp env.example .env

# Edit .env with your preferences
nano .env
```

### 3. Start Services

```bash
# Development environment
./start.sh development

# Wait for services to start (~30 seconds)
# Access JupyterLab: http://localhost:8888
# Access Kedro Viz: http://localhost:4141
```

## Detailed Setup

### Environment Variables

Edit `.env` file with your configuration:

```bash
# Kedro Configuration
KEDRO_ENV=local
KEDRO_LOGGING_LEVEL=INFO

# Jupyter Configuration  
JUPYTER_TOKEN=your-secure-token

# Database Configuration (if using PostgreSQL)
POSTGRES_DB=spaceflights
POSTGRES_USER=kedro
POSTGRES_PASSWORD=your-secure-password

# Airflow Configuration (if using Airflow)
AIRFLOW_FERNET_KEY=generate-with-command-below
```

#### Generate Fernet Key

```bash
pip install cryptography
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### Docker Compose Profiles

The project uses profiles to manage different environments:

```bash
# Development (JupyterLab + Kedro Viz)
docker-compose --profile development up -d

# Production (Automated execution)
docker-compose --profile production up -d

# With database
docker-compose --profile development --profile database up -d

# With cache
docker-compose --profile development --profile cache up -d

# Full stack
docker-compose --profile development --profile database --profile cache up -d
```

### Airflow Setup

```bash
# Start Airflow services
./start.sh airflow

# Or manually
docker-compose -f docker-compose.airflow.yml up -d

# Access Airflow UI
open http://localhost:8080
# Username: admin
# Password: admin
```

## Optional: Local Development (without Docker)

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

### 3. Run Kedro

```bash
# Run pipeline
kedro run

# Run specific pipeline
kedro run --pipeline data_processing

# Start Kedro Viz
kedro viz run
```

## Optional: Custom Docker Override

If you need custom configurations:

```bash
# Copy template
cp docker-compose.override.yml.example docker-compose.override.yml

# Edit as needed
nano docker-compose.override.yml

# This file is automatically loaded and gitignored
```

## Verification

### Check Services

```bash
# List running containers
docker-compose ps

# View logs
docker-compose logs -f

# Check specific service
docker-compose logs jupyter-lab
```

### Test Pipeline

```bash
# Execute test pipeline
docker-compose exec jupyter-lab kedro run --pipeline data_processing

# Expected output: Pipeline execution successful
```

## Troubleshooting

See [troubleshooting.md](./troubleshooting.md) for common issues.

## Next Steps

- [Pipeline Documentation](./pipelines.md)
- [Docker Guide](./docker.md)
- [Airflow Guide](./airflow.md)
- [Architecture](../ARCHITECTURE.md)

