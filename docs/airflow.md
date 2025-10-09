# ✈️ Apache Airflow Integration Guide

## Overview

This project integrates Apache Airflow for pipeline orchestration, allowing scheduled and automated execution of Kedro pipelines.

## Architecture

```
Airflow DAGs → KedroOperator → Kedro Session → Pipeline Execution
```

### Components

- **Airflow Webserver**: UI for DAG management (port 8080)
- **Airflow Scheduler**: Executes DAGs on schedule
- **Airflow Database**: PostgreSQL for metadata
- **KedroOperator**: Custom operator to run Kedro nodes

## Starting Airflow

```bash
# Using start script
./start.sh airflow

# Or manually
docker-compose -f docker-compose.airflow.yml up -d
```

### Access

- **URL**: http://localhost:8080
- **Username**: `admin`
- **Password**: `admin`

## DAGs

### Available DAGs

1. **spaceflights_dag.py**: Complete pipeline
2. **spaceflights_data_processing_dag.py**: Data processing only
3. **spaceflights_reporting_dag.py**: Reporting only

### DAG Structure

```python
with DAG(
    dag_id="spaceflights",
    start_date=datetime(2025,10,1),
    schedule_interval="@daily",  # or cron expression
    catchup=False,
) as dag:
    task1 = KedroOperator(...)
    task2 = KedroOperator(...)
    
    task1 >> task2  # Set dependencies
```

## KedroOperator

### Custom Operator

The `KedroOperator` integrates Kedro with Airflow:

```python
class KedroOperator(BaseOperator):
    def __init__(
        self,
        package_name: str,      # "spaceflights"
        pipeline_name: str,     # "__default__" or specific pipeline
        node_name: str,         # Kedro node name
        project_path: Path,     # /app
        env: str,               # "local", "production"
        conf_source: str,       # path to conf/
        *args, **kwargs
    ):
        ...
    
    def execute(self, context):
        configure_project(self.package_name)
        with KedroSession.create(...) as session:
            session.run(self.pipeline_name, node_names=self.node_name)
```

### Usage Example

```python
preprocess_task = KedroOperator(
    task_id="preprocess-companies",
    package_name="spaceflights",
    pipeline_name="data_processing",
    node_name="preprocess_companies_node",
    project_path="/app",
    env="local",
    conf_source="/app/conf",
)
```

## Creating New DAGs

### 1. Create DAG File

Create `dags/my_new_dag.py`:

```python
from datetime import datetime, timedelta
from pathlib import Path
from airflow import DAG
from airflow.models import BaseOperator
from kedro.framework.session import KedroSession
from kedro.framework.project import configure_project

# Import or define KedroOperator

# Kedro settings
env = "local"
pipeline_name = "my_pipeline"
project_path = Path("/app")
package_name = "spaceflights"
conf_source = Path("/app/conf")

with DAG(
    dag_id="my_new_dag",
    start_date=datetime(2025, 10, 1),
    schedule_interval="@daily",
    catchup=False,
    default_args={
        "owner": "airflow",
        "retries": 1,
        "retry_delay": timedelta(minutes=5)
    }
) as dag:
    
    task1 = KedroOperator(
        task_id="task1",
        package_name=package_name,
        pipeline_name=pipeline_name,
        node_name="node1",
        project_path=project_path,
        env=env,
        conf_source=conf_source,
    )
    
    task2 = KedroOperator(
        task_id="task2",
        package_name=package_name,
        pipeline_name=pipeline_name,
        node_name="node2",
        project_path=project_path,
        env=env,
        conf_source=conf_source,
    )
    
    task1 >> task2  # task2 depends on task1
```

### 2. Mount DAG File

DAGs directory is already mounted in `docker-compose.airflow.yml`:

```yaml
volumes:
  - ./dags:/opt/airflow/dags
```

Just add your new DAG file to `dags/` directory.

### 3. Verify DAG

```bash
# List DAGs
docker-compose -f docker-compose.airflow.yml exec airflow-webserver airflow dags list

# Test DAG
docker-compose -f docker-compose.airflow.yml exec airflow-webserver \
  airflow dags test my_new_dag 2025-10-01
```

## Schedule Intervals

### Common Schedules

```python
schedule_interval="@once"      # Run once
schedule_interval="@hourly"    # Every hour
schedule_interval="@daily"     # Every day at midnight
schedule_interval="@weekly"    # Every week
schedule_interval="@monthly"   # Every month
```

### Cron Expressions

```python
schedule_interval="0 */2 * * *"    # Every 2 hours
schedule_interval="30 8 * * 1-5"   # 8:30 AM, Mon-Fri
schedule_interval="0 0 * * 0"      # Weekly on Sunday
```

## DAG Configuration

### Default Arguments

```python
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": ["admin@example.com"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "execution_timeout": timedelta(hours=2),
}
```

### DAG Parameters

```python
with DAG(
    dag_id="my_dag",
    start_date=datetime(2025, 10, 1),
    schedule_interval="@daily",
    catchup=False,              # Don't backfill
    max_active_runs=1,          # One run at a time
    default_args=default_args,
    tags=["kedro", "ml"],
    description="My ML pipeline",
) as dag:
    ...
```

## Task Dependencies

### Linear Dependencies

```python
task1 >> task2 >> task3
# or
task1.set_downstream(task2)
task2.set_downstream(task3)
```

### Parallel Tasks

```python
task1 >> [task2, task3] >> task4
#      /              \
# task1 → task2 → task4
#      \              /
#       → task3 -----
```

### Complex Dependencies

```python
from airflow.utils.task_group import TaskGroup

with TaskGroup("processing") as processing:
    preprocess_companies = KedroOperator(...)
    preprocess_shuttles = KedroOperator(...)

with TaskGroup("training") as training:
    train_model = KedroOperator(...)
    evaluate_model = KedroOperator(...)

processing >> training
```

## Monitoring

### Web UI

Access http://localhost:8080 to:
- View DAG status
- Trigger manual runs
- View logs
- Monitor task duration
- Check task dependencies

### DAG States

- **Success**: All tasks completed successfully
- **Running**: DAG is currently executing
- **Failed**: One or more tasks failed
- **Queued**: Waiting to start

### Task States

- **Success**: Task completed
- **Running**: Task executing
- **Failed**: Task failed
- **Retry**: Task will retry
- **Skipped**: Task was skipped

## Logging

### View Logs in UI

1. Click on DAG
2. Click on Task
3. Click "Log" button

### View Logs via CLI

```bash
# View task logs
docker-compose -f docker-compose.airflow.yml exec airflow-scheduler \
  airflow tasks logs my_dag my_task 2025-10-01
```

### Log Location

```
logs/
└── dag_id=my_dag/
    └── run_id=manual__2025-10-01T00:00:00+00:00/
        └── task_id=my_task/
            └── attempt=1.log
```

## Debugging

### Test DAG Syntax

```bash
docker-compose -f docker-compose.airflow.yml exec airflow-webserver \
  python /opt/airflow/dags/my_dag.py
```

### Test Task Execution

```bash
docker-compose -f docker-compose.airflow.yml exec airflow-scheduler \
  airflow tasks test my_dag my_task 2025-10-01
```

### Check DAG Structure

```bash
docker-compose -f docker-compose.airflow.yml exec airflow-webserver \
  airflow dags show my_dag
```

## Best Practices

1. **Idempotent Tasks**: Tasks should produce same result when rerun
2. **Small Tasks**: Break large operations into smaller tasks
3. **Error Handling**: Add retries and alerts
4. **Resource Management**: Set execution timeouts
5. **Documentation**: Add descriptions and tags
6. **Testing**: Test DAGs before deployment
7. **Monitoring**: Set up alerts for failures
8. **Logging**: Add meaningful log messages

## Integration with Kedro

### Automatic DAG Generation

You can generate Airflow DAGs from Kedro pipelines:

```bash
# Install kedro-airflow
pip install kedro-airflow

# Generate DAG
kedro airflow create --pipeline data_processing
```

### Manual DAG Creation

For more control, create DAGs manually using `KedroOperator` as shown in examples.

## Environment Variables

Set in `docker-compose.airflow.yml`:

```yaml
environment:
  - AIRFLOW__CORE__EXECUTOR=LocalExecutor
  - AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://...
  - AIRFLOW__CORE__FERNET_KEY=${AIRFLOW_FERNET_KEY}
  - KEDRO_HOME=/app
  - PYTHONPATH=/app/src
```

## Troubleshooting

### DAG Not Appearing

```bash
# Check DAG folder
docker-compose -f docker-compose.airflow.yml exec airflow-webserver \
  ls -la /opt/airflow/dags

# Check for syntax errors
docker-compose -f docker-compose.airflow.yml exec airflow-webserver \
  python /opt/airflow/dags/my_dag.py

# Restart scheduler
docker-compose -f docker-compose.airflow.yml restart airflow-scheduler
```

### Database Issues

```bash
# Reset database
docker-compose -f docker-compose.airflow.yml down -v
docker-compose -f docker-compose.airflow.yml up -d
```

### Task Failures

1. Check task logs in UI
2. Verify Kedro pipeline works: `kedro run --pipeline xyz`
3. Check environment variables
4. Verify file paths and permissions

## See Also

- [Setup Guide](./setup.md)
- [Pipelines Documentation](./pipelines.md)
- [Troubleshooting](./troubleshooting.md)
- [Airflow Documentation](https://airflow.apache.org/docs/)
- [Kedro-Airflow Plugin](https://github.com/kedro-org/kedro-plugins/tree/main/kedro-airflow)

