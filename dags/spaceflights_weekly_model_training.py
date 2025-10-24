"""
Spaceflights Weekly Model Training

Retrains ML models weekly with accumulated data.
This DAG demonstrates scheduled model retraining workflow.

Schedule: Every Sunday at 3 AM UTC
Author: MLOps Team
"""

from __future__ import annotations

from datetime import timedelta

from airflow import DAG
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.sensors.external_task import ExternalTaskSensor
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
# Weekly Model Training Pipeline

Retrains models with accumulated data from the past week.

## Purpose

Weekly retraining ensures models stay current with latest data patterns.

## Dependencies

Waits for latest data processing to complete before training.

## Pipeline

1. **Wait for Data**: Ensure fresh data is available
2. **Split Data**: Prepare train/test sets
3. **Train Model**: Fit model with new data
4. **Evaluate**: Validate model performance
5. **Generate Reports**: Create performance visualizations

## Schedule

Every Sunday at 3:00 AM UTC (weekly retraining cycle)

## Model Versioning

Each run creates a new versioned model in `data/06_models/`

## SLAs

- Training: 1 hour
- Evaluation: 30 minutes
"""

with DAG(
    dag_id="spaceflights_weekly_model_training",
    description="Weekly model retraining and evaluation",
    doc_md=DAG_DOC_MD,
    start_date=DAG_START_DATE,
    schedule="0 3 * * 0",  # Every Sunday at 3 AM
    catchup=False,
    max_active_runs=1,
    default_args=DEFAULT_DAG_ARGS,
    tags=TAGS["ML"] + TAGS["PRODUCTION"],
) as dag:
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end", trigger_rule="none_failed")

    # Wait for latest data processing to complete
    wait_for_data = ExternalTaskSensor(
        task_id="wait_for_latest_data",
        external_dag_id="spaceflights_daily_data_processing",
        external_task_id="end",
        timeout=3600,  # Wait up to 1 hour
        mode="reschedule",  # Free up worker slot while waiting
        doc_md="Waits for the latest data processing DAG to complete",
    )

    # =====================================================
    # MODEL TRAINING STAGE
    # =====================================================
    with TaskGroup("model_training", tooltip="Train and evaluate models") as training:
        split_data_task = KedroOperator(
            task_id="split_data",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="data_science",
            node_name="split_data_node",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
            doc_md="Split data into train/test sets",
            sla=timedelta(minutes=5),
        )

        train_model_task = KedroOperator(
            task_id="train_model",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="data_science",
            node_name="train_model_node",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
            doc_md="Train regression model on training data",
            sla=timedelta(minutes=45),
        )

        evaluate_model_task = KedroOperator(
            task_id="evaluate_model",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="data_science",
            node_name="evaluate_model_node",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
            doc_md="Evaluate model performance on test data",
            sla=timedelta(minutes=15),
        )

        # Training dependencies
        split_data_task >> train_model_task >> evaluate_model_task

    # =====================================================
    # REPORTING STAGE
    # =====================================================
    with TaskGroup(
        "reporting", tooltip="Generate model performance reports"
    ) as reporting:
        plot_capacity_exp = KedroOperator(
            task_id="plot_capacity_express",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="reporting",
            node_name="compare_passenger_capacity_exp",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
            sla=timedelta(minutes=5),
        )

        plot_capacity_go = KedroOperator(
            task_id="plot_capacity_go",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="reporting",
            node_name="compare_passenger_capacity_go",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
            sla=timedelta(minutes=5),
        )

        confusion_matrix = KedroOperator(
            task_id="confusion_matrix",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="reporting",
            node_name="create_confusion_matrix",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
            sla=timedelta(minutes=5),
        )

        # Reporting tasks run in parallel
        [plot_capacity_exp, plot_capacity_go, confusion_matrix]

    # =====================================================
    # COMPLETE PIPELINE FLOW
    # =====================================================
    start >> wait_for_data >> training >> reporting >> end
