# ✈️ Airflow DAGs - Spaceflights

## Overview

This directory contains Apache Airflow DAGs for orchestrating Kedro ML pipelines.

## DAG Structure

```
dags/
├── operators/                  # Custom operators
│   ├── __init__.py
│   └── kedro_operator.py      # KedroOperator for Kedro integration
├── config.py                   # Common configuration
├── spaceflights_ml_pipeline.py # Complete ML workflow (daily)
├── spaceflights_daily_data_processing.py  # Data processing (every 4h)
├── spaceflights_weekly_model_training.py  # Model retraining (weekly)
└── spaceflights_on_demand.py  # Manual trigger DAG
```

## Available DAGs

### 1. spaceflights_ml_pipeline
**Schedule**: Daily at 2 AM UTC  
**Purpose**: Complete end-to-end ML workflow  
**Stages**: Data Processing → Model Training → Reporting

```python
# Execution flow
start → data_processing → data_science → reporting → end
```

**Use case**: Production daily ML pipeline

---

### 2. spaceflights_daily_data_processing
**Schedule**: Every 4 hours  
**Purpose**: Continuous data ingestion and processing  
**Stages**: Data Processing only

```python
# Execution flow
start → preprocess_data → create_model_input → end
```

**Use case**: Keep datasets fresh with new data

---

### 3. spaceflights_weekly_model_training
**Schedule**: Every Sunday at 3 AM UTC  
**Purpose**: Weekly model retraining  
**Stages**: Model Training → Reporting  
**Dependencies**: Waits for latest data processing

```python
# Execution flow
start → wait_for_data → train_model → evaluate → reporting → end
```

**Use case**: Regular model updates with accumulated data

---

### 4. spaceflights_on_demand
**Schedule**: Manual trigger only  
**Purpose**: Ad-hoc experiments and testing  
**Stages**: Complete pipeline

```python
# Execution flow
start → data_processing → model_training → reporting → end
```

**Use case**: Testing, experiments, parameter tuning

---

## KedroOperator

Custom operator located in `operators/kedro_operator.py`

### Usage

```python
from operators import KedroOperator

task = KedroOperator(
    task_id="my_task",
    package_name="spaceflights",
    pipeline_name="data_processing",
    node_name="preprocess_companies_node",
    project_path="/app",
    env="local",
    conf_source="/app/conf",
)
```

### Features

- Runs Kedro nodes from Airflow
- Automatic error handling and logging
- Integration with Airflow monitoring
- Supports single node or multiple nodes
- Configurable environment and parameters

---

## Configuration

Common settings in `config.py`:

```python
KEDRO_PACKAGE_NAME = "spaceflights"
KEDRO_PROJECT_PATH = Path("/app")
KEDRO_ENV = "local"

DEFAULT_DAG_ARGS = {
    "owner": "mlops-team",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": True,
}
```

---

## Best Practices

### 1. Use TaskGroups
Organize related tasks for better visualization:

```python
with TaskGroup("data_processing") as processing:
    task1 = KedroOperator(...)
    task2 = KedroOperator(...)
```

### 2. Set SLAs
Define expected execution times:

```python
task = KedroOperator(
    ...,
    sla=timedelta(minutes=30),
)
```

### 3. Add Documentation
Use doc_md for inline documentation:

```python
task = KedroOperator(
    ...,
    doc_md="### Task Description\nDetailed explanation...",
)
```

### 4. Configure Retries
Set appropriate retry policies:

```python
default_args = {
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "retry_exponential_backoff": True,
}
```

### 5. Use Sensors
Wait for dependencies:

```python
from airflow.sensors.external_task import ExternalTaskSensor

wait_task = ExternalTaskSensor(
    task_id="wait_for_data",
    external_dag_id="upstream_dag",
    external_task_id="end",
)
```

---

## Adding New DAGs

### 1. Create DAG File

Create `dags/my_new_dag.py`:

```python
from operators import KedroOperator
from config import *

with DAG(
    dag_id="my_new_dag",
    schedule_interval="@daily",
    default_args=DEFAULT_DAG_ARGS,
    tags=TAGS["ML"],
) as dag:
    
    task = KedroOperator(
        task_id="my_task",
        package_name=KEDRO_PACKAGE_NAME,
        pipeline_name="my_pipeline",
        node_name="my_node",
        project_path=KEDRO_PROJECT_PATH,
        env=KEDRO_ENV,
        conf_source=KEDRO_CONF_SOURCE,
    )
```

### 2. Test DAG

```bash
# Check syntax
docker-compose -f docker-compose.airflow.yml exec airflow-webserver \
  python /opt/airflow/dags/my_new_dag.py

# Test DAG execution
docker-compose -f docker-compose.airflow.yml exec airflow-scheduler \
  airflow dags test my_new_dag 2025-10-01
```

### 3. Monitor in UI

Access http://localhost:8080 to see your new DAG.

---

## Monitoring and Alerts

### SLA Monitoring

DAGs include SLA definitions for time expectations:

```python
task = KedroOperator(
    ...,
    sla=timedelta(minutes=30),  # Alert if task takes >30min
)
```

### Email Alerts

Configure in `default_args`:

```python
default_args = {
    "email": ["team@spaceflights.com"],
    "email_on_failure": True,
    "email_on_retry": False,
}
```

### Execution Timeout

Prevent hanging tasks:

```python
default_args = {
    "execution_timeout": timedelta(hours=2),
}
```

---

## Schedule Examples

```python
# Common schedules
schedule_interval="@once"           # Run once
schedule_interval="@hourly"         # Every hour
schedule_interval="@daily"          # Daily at midnight
schedule_interval="@weekly"         # Every Monday
schedule_interval="@monthly"        # First of month

# Cron expressions
schedule_interval="0 2 * * *"       # Daily at 2 AM
schedule_interval="0 */4 * * *"     # Every 4 hours
schedule_interval="0 8 * * 1-5"     # 8 AM Monday-Friday
schedule_interval="0 3 * * 0"       # Sunday at 3 AM

# Manual only
schedule_interval=None              # No automatic schedule
```

---

## Debugging

### View DAG Structure

```bash
# List all DAGs
docker-compose -f docker-compose.airflow.yml exec airflow-webserver \
  airflow dags list

# Show DAG details
docker-compose -f docker-compose.airflow.yml exec airflow-webserver \
  airflow dags show spaceflights_ml_pipeline
```

### Test Task Execution

```bash
# Test single task
docker-compose -f docker-compose.airflow.yml exec airflow-scheduler \
  airflow tasks test spaceflights_ml_pipeline start 2025-10-01
```

### View Logs

```bash
# View task logs
docker-compose -f docker-compose.airflow.yml exec airflow-scheduler \
  airflow tasks logs spaceflights_ml_pipeline preprocess_companies 2025-10-01
```

---

## Troubleshooting

### DAG Not Appearing

1. Check syntax: `python /opt/airflow/dags/my_dag.py`
2. Check logs: `docker-compose -f docker-compose.airflow.yml logs airflow-scheduler`
3. Restart scheduler: `docker-compose -f docker-compose.airflow.yml restart airflow-scheduler`

### Import Errors

Ensure `operators/` directory has `__init__.py` and correct imports.

### Task Failures

1. Check Airflow UI for error logs
2. Verify Kedro pipeline works: `kedro run --pipeline xyz`
3. Check environment variables and paths

---

## See Also

- [Airflow Guide](../docs/airflow.md)
- [Pipelines Documentation](../docs/pipelines.md)
- [Troubleshooting](../docs/troubleshooting.md)
- [Airflow Documentation](https://airflow.apache.org/docs/)

