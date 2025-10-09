"""
Spaceflights On-Demand Pipeline

Manual trigger for ad-hoc pipeline execution.
Useful for testing, experiments, and one-off runs.

Schedule: Manual trigger only
Author: MLOps Team
"""
from __future__ import annotations

from datetime import timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator
from airflow.utils.task_group import TaskGroup

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
# On-Demand ML Pipeline

Manually triggered pipeline for experiments and ad-hoc runs.

## Use Cases

- Testing new code changes
- Running experiments with different parameters
- One-off model training
- Data exploration and validation

## Features

- Can run complete pipeline or individual stages
- Configurable via Airflow UI
- No schedule - trigger manually when needed

## How to Trigger

1. Go to Airflow UI: http://localhost:8080
2. Find `spaceflights_on_demand` DAG
3. Click "Trigger DAG" button
4. Optionally provide custom configuration

## Monitoring

Monitor execution in real-time via:
- Airflow UI: http://localhost:8080
- Kedro Viz: http://localhost:4141
"""

# Custom args for on-demand runs
on_demand_args = DEFAULT_DAG_ARGS.copy()
on_demand_args.update({
    "retries": 1,  # Less retries for manual runs
    "retry_delay": timedelta(minutes=1),
})

with DAG(
    dag_id="spaceflights_on_demand",
    description="Manual trigger for ad-hoc pipeline execution",
    doc_md=DAG_DOC_MD,
    start_date=DAG_START_DATE,
    schedule_interval=None,  # Manual trigger only
    catchup=False,
    max_active_runs=3,  # Allow multiple parallel manual runs
    default_args=on_demand_args,
    tags=TAGS["ML"] + TAGS["DEVELOPMENT"] + ["on-demand", "manual"],
) as dag:

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end", trigger_rule="none_failed_min_one_success")

    # =====================================================
    # DATA PROCESSING
    # =====================================================
    with TaskGroup("data_processing") as data_processing:
        
        preprocess_companies = KedroOperator(
            task_id="preprocess_companies",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="data_processing",
            node_name="preprocess_companies_node",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
        )

        preprocess_shuttles = KedroOperator(
            task_id="preprocess_shuttles",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="data_processing",
            node_name="preprocess_shuttles_node",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
        )

        create_model_input = KedroOperator(
            task_id="create_model_input_table",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="data_processing",
            node_name="create_model_input_table_node",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
        )

        [preprocess_companies, preprocess_shuttles] >> create_model_input

    # =====================================================
    # MODEL TRAINING
    # =====================================================
    with TaskGroup("model_training") as training:
        
        split_data = KedroOperator(
            task_id="split_data",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="data_science",
            node_name="split_data_node",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
        )

        train_model = KedroOperator(
            task_id="train_model",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="data_science",
            node_name="train_model_node",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
        )

        evaluate_model = KedroOperator(
            task_id="evaluate_model",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="data_science",
            node_name="evaluate_model_node",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
        )

        split_data >> train_model >> evaluate_model

    # =====================================================
    # REPORTING
    # =====================================================
    with TaskGroup("reporting") as reporting:
        
        generate_plots = KedroOperator(
            task_id="generate_all_plots",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="reporting",
            node_name=[
                "compare_passenger_capacity_exp",
                "compare_passenger_capacity_go",
                "create_confusion_matrix",
            ],
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
        )

    # Complete pipeline flow
    start >> data_processing >> training >> reporting >> end

