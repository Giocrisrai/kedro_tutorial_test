"""
Spaceflights Daily Data Processing

Runs every 4 hours to process new incoming data.
This DAG is designed for continuous data ingestion scenarios.

Schedule: Every 4 hours
Author: MLOps Team
"""
from __future__ import annotations

from datetime import timedelta

from airflow import DAG
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.sdk import TaskGroup

from config import (
    DAG_START_DATE,
    DEFAULT_DAG_ARGS,
    KEDRO_CONF_SOURCE,
    KEDRO_ENV,
    KEDRO_PACKAGE_NAME,
    KEDRO_PROJECT_PATH,
    TAGS,
)
from operators import KedroOperator

DAG_DOC_MD = """
# Daily Data Processing Pipeline

Continuous data processing for incoming data.

## Purpose

Process new data as it arrives, keeping datasets up-to-date for model training.

## Schedule

Runs every 4 hours to catch new data batches.

## Tasks

1. **Preprocess Companies**: Clean company information
2. **Preprocess Shuttles**: Process shuttle data
3. **Create Model Input**: Join datasets for ML

## SLAs

Total processing time should be under 30 minutes.

## Alerts

Notifications sent on:
- Task failure
- SLA miss
- Pipeline completion (success)
"""

# Custom default args for frequent runs
frequent_run_args = DEFAULT_DAG_ARGS.copy()
frequent_run_args.update({
    "retries": 3,  # More retries for frequent jobs
    "retry_delay": timedelta(minutes=2),  # Shorter retry delay
})

with DAG(
    dag_id="spaceflights_daily_data_processing",
    description="Process new data every 4 hours",
    doc_md=DAG_DOC_MD,
    start_date=DAG_START_DATE,
    schedule="0 */4 * * *",  # Every 4 hours
    catchup=False,
    max_active_runs=1,
    default_args=frequent_run_args,
    tags=TAGS["ETL"] + TAGS["PRODUCTION"],
) as dag:

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end", trigger_rule="none_failed")

    with TaskGroup("data_processing", tooltip="Process incoming data") as processing:
        
        preprocess_companies = KedroOperator(
            task_id="preprocess_companies",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="data_processing",
            node_name="preprocess_companies_node",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
            sla=timedelta(minutes=10),
        )

        preprocess_shuttles = KedroOperator(
            task_id="preprocess_shuttles",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="data_processing",
            node_name="preprocess_shuttles_node",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
            sla=timedelta(minutes=10),
        )

        create_model_input = KedroOperator(
            task_id="create_model_input_table",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="data_processing",
            node_name="create_model_input_table_node",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
            sla=timedelta(minutes=10),
        )

        # Process companies and shuttles in parallel, then join
        [preprocess_companies, preprocess_shuttles] >> create_model_input

    # Pipeline flow
    start >> processing >> end

