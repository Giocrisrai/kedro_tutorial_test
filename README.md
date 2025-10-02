# spaceflights

[![Powered by Kedro](https://img.shields.io/badge/powered_by-kedro-ffc900?logo=kedro)](https://kedro.org)

## Overview

This is your new Kedro project, which was generated using `kedro 1.0.0`.

Take a look at the [Kedro documentation](https://docs.kedro.org) to get started.

## Rules and guidelines

In order to get the best out of the template:

* Don't remove any lines from the `.gitignore` file we provide
* Make sure your results can be reproduced by following a [data engineering convention](https://docs.kedro.org/en/stable/faq/faq.html#what-is-data-engineering-convention)
* Don't commit data to your repository
* Don't commit any credentials or your local configuration to your repository. Keep all your credentials and local configuration in `conf/local/`

## How to install dependencies

Declare any dependencies in `requirements.txt` for `pip` installation.

To install them, run:

```
pip install -r requirements.txt
```

## 🐳 Docker Setup (Recomendado)

Este proyecto está configurado para ejecutarse en Docker y Docker Compose, proporcionando un entorno de desarrollo y producción consistente.

### Inicio Rápido con Docker

```bash
# Iniciar entorno de desarrollo completo
./start.sh development

# O usar docker-compose directamente
docker-compose --profile development up -d
```

### Servicios Disponibles

| Servicio | URL | Descripción |
|----------|-----|-------------|
| JupyterLab | http://localhost:8888 | Entorno de desarrollo interactivo |
| Kedro Viz | http://localhost:4141 | Visualización de pipelines |
| PostgreSQL | localhost:5432 | Base de datos (opcional) |
| Redis | localhost:6379 | Cache (opcional) |

### Comandos Útiles

```bash
# Ver logs
docker-compose logs -f

# Acceso interactivo
docker-compose exec jupyter-lab bash

# Ejecutar pipeline específico
./scripts/run-pipeline.sh data_processing

# Detener servicios
docker-compose down
```

Para más información detallada, consulta [README-Docker.md](README-Docker.md).

## How to run your Kedro pipeline

### Con Docker (Recomendado)
```bash
# Pipeline completo
docker-compose exec jupyter-lab kedro run

# Pipeline específico
docker-compose exec jupyter-lab kedro run --pipeline data_processing
```

### Sin Docker
You can run your Kedro project with:

```
kedro run
```

## How to test your Kedro project

Have a look at the files `tests/test_run.py` and `tests/pipelines/data_science/test_pipeline.py` for instructions on how to write your tests. Run the tests as follows:

```
pytest
```

You can configure the coverage threshold in your project's `pyproject.toml` file under the `[tool.coverage.report]` section.

## Project dependencies

To see and update the dependency requirements for your project use `requirements.txt`. You can install the project requirements with `pip install -r requirements.txt`.

[Further information about project dependencies](https://docs.kedro.org/en/stable/kedro_project_setup/dependencies.html#project-specific-dependencies)

## How to work with Kedro and notebooks

> Note: Using `kedro jupyter` or `kedro ipython` to run your notebook provides these variables in scope: `catalog`, `context`, `pipelines` and `session`.
>
> Jupyter, JupyterLab, and IPython are already included in the project requirements by default, so once you have run `pip install -r requirements.txt` you will not need to take any extra steps before you use them.

### Jupyter
To use Jupyter notebooks in your Kedro project, you need to install Jupyter:

```
pip install jupyter
```

After installing Jupyter, you can start a local notebook server:

```
kedro jupyter notebook
```

### JupyterLab
To use JupyterLab, you need to install it:

```
pip install jupyterlab
```

You can also start JupyterLab:

```
kedro jupyter lab
```

### IPython
And if you want to run an IPython session:

```
kedro ipython
```

### How to ignore notebook output cells in `git`
To automatically strip out all output cell contents before committing to `git`, you can use tools like [`nbstripout`](https://github.com/kynan/nbstripout). For example, you can add a hook in `.git/config` with `nbstripout --install`. This will run `nbstripout` before anything is committed to `git`.

> *Note:* Your output cells will be retained locally.

## 🚀 Entornos de Desarrollo y Producción

### 🛠️ Desarrollo
```bash
# Iniciar entorno de desarrollo
./scripts/start-dev.sh

# Servicios disponibles:
# - JupyterLab: http://localhost:8888
# - Kedro Viz: http://localhost:4141
# - PostgreSQL: localhost:5432 (opcional)
# - Redis: localhost:6379 (opcional)
```

### 🏭 Producción
```bash
# Iniciar entorno de producción
./scripts/start-prod.sh

# Servicios disponibles:
# - Kedro Producción: Ejecuta pipelines automáticamente
# - Scheduler: Ejecuta pipelines cada hora
# - Kedro Viz: http://localhost:4141
# - Logs: Volúmenes persistentes
```

### 📊 Gestión de Pipelines
```bash
# Ejecutar pipeline específico
./scripts/run-pipeline.sh development data_processing
./scripts/run-pipeline.sh production all

# Monitoreo de servicios
./scripts/monitor.sh development
./scripts/monitor.sh production
```

### 🔧 Comandos Avanzados
```bash
# Ver logs en tiempo real
docker-compose --profile development logs -f
docker-compose --profile production logs -f

# Acceso interactivo
docker-compose exec jupyter-lab bash  # desarrollo
docker-compose exec kedro-prod bash   # producción

# Ejecutar pipeline manual
docker-compose exec kedro-prod kedro run --pipeline data_processing
```

## Package your Kedro project

[Further information about building project documentation and packaging your project](https://docs.kedro.org/en/stable/tutorial/package_a_project.html)
