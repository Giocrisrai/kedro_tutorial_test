"""
Common configuration for all Airflow DAGs in the Spaceflights project.
"""
from datetime import datetime, timedelta
from pathlib import Path

# Kedro Project Configuration
KEDRO_PACKAGE_NAME = "spaceflights"
KEDRO_PROJECT_PATH = Path("/app")
KEDRO_ENV = "local"
KEDRO_CONF_SOURCE = str(KEDRO_PROJECT_PATH / "conf")

# Common DAG default arguments
DEFAULT_DAG_ARGS = {
    "owner": "mlops-team",
    "depends_on_past": False,
    "email": ["airflow@spaceflights.com"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "retry_exponential_backoff": True,
    "max_retry_delay": timedelta(minutes=30),
    "execution_timeout": timedelta(hours=2),
}

# Start date for all DAGs
DAG_START_DATE = datetime(2025, 10, 1)

# Tags for DAG categorization
TAGS = {
    "ML": ["ml", "machine-learning", "kedro"],
    "ETL": ["etl", "data-processing", "kedro"],
    "REPORTING": ["reporting", "visualization", "kedro"],
    "PRODUCTION": ["production", "automated"],
    "DEVELOPMENT": ["development", "testing"],
}

