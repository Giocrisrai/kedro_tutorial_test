"""
Spaceflights ML Pipeline - Complete End-to-End Workflow

This DAG orchestrates the complete machine learning workflow:
1. Data Processing: Clean and prepare data
2. Data Science: Train and evaluate models
3. Reporting: Generate visualizations

Schedule: Daily at 2 AM UTC
Author: MLOps Team
"""
from __future__ import annotations

from datetime import timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
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

# DAG documentation
DAG_DOC_MD = """
# Spaceflights ML Pipeline

Complete end-to-end machine learning workflow for the Spaceflights project.

## Pipeline Stages

### 1. Data Processing
- Preprocess company data
- Preprocess shuttle data
- Create model input table

### 2. Data Science
- Split data into train/test sets
- Train regression model
- Evaluate model performance

### 3. Reporting
- Generate passenger capacity visualizations
- Create confusion matrix
- Export reports

## Schedule

Runs daily at 2:00 AM UTC to process previous day's data.

## SLAs

- Data Processing: 30 minutes
- Model Training: 1 hour
- Reporting: 15 minutes

## Monitoring

Check Kedro Viz for pipeline visualization: http://localhost:4141
"""

# Define the DAG
with DAG(
    dag_id="spaceflights_ml_pipeline",
    description="Complete ML pipeline: data processing → training → reporting",
    doc_md=DAG_DOC_MD,
    start_date=DAG_START_DATE,
    schedule_interval="0 2 * * *",  # Daily at 2 AM UTC
    catchup=False,
    max_active_runs=1,  # One run at a time
    default_args=DEFAULT_DAG_ARGS,
    tags=TAGS["ML"] + TAGS["PRODUCTION"],
) as dag:

    # Start and end markers
    start = EmptyOperator(
        task_id="start",
        doc_md="Pipeline execution start marker",
    )

    end = EmptyOperator(
        task_id="end",
        doc_md="Pipeline execution end marker",
        trigger_rule="none_failed",  # Run if no upstream tasks failed
    )

    # =====================================================
    # DATA PROCESSING STAGE
    # =====================================================
    with TaskGroup("data_processing", tooltip="Clean and prepare raw data") as data_processing:
        
        preprocess_companies = KedroOperator(
            task_id="preprocess_companies",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="data_processing",
            node_name="preprocess_companies_node",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
            doc_md="""
            ### Preprocess Companies
            
            Cleans and standardizes company data:
            - Removes null values
            - Converts boolean columns
            - Standardizes company names
            
            **Input**: `companies.csv`
            **Output**: `preprocessed_companies.parquet`
            """,
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
            doc_md="""
            ### Preprocess Shuttles
            
            Cleans and prepares shuttle data:
            - Extracts engine information
            - Removes missing values
            - Standardizes formats
            
            **Input**: `shuttles.xlsx`
            **Output**: `preprocessed_shuttles.parquet`
            """,
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
            doc_md="""
            ### Create Model Input Table
            
            Joins preprocessed data for model training:
            - Merges companies and shuttles data
            - Adds review information
            - Creates final training dataset
            
            **Inputs**: preprocessed data + reviews
            **Output**: `model_input_table.parquet`
            """,
            sla=timedelta(minutes=10),
        )

        # Dependencies within data processing
        [preprocess_companies, preprocess_shuttles] >> create_model_input

    # =====================================================
    # DATA SCIENCE STAGE
    # =====================================================
    with TaskGroup("data_science", tooltip="Train and evaluate ML models") as data_science:
        
        split_data = KedroOperator(
            task_id="split_data",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="data_science",
            node_name="split_data_node",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
            doc_md="""
            ### Split Data
            
            Splits data into training and test sets:
            - Applies configured test_size ratio
            - Uses random_state for reproducibility
            
            **Input**: `model_input_table.parquet`
            **Outputs**: X_train, X_test, y_train, y_test
            """,
            sla=timedelta(minutes=5),
        )

        train_model = KedroOperator(
            task_id="train_model",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="data_science",
            node_name="train_model_node",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
            doc_md="""
            ### Train Model
            
            Trains linear regression model:
            - Uses training data
            - Fits model parameters
            - Saves versioned model
            
            **Inputs**: X_train, y_train
            **Output**: `regressor.pickle` (versioned)
            """,
            sla=timedelta(minutes=30),
        )

        evaluate_model = KedroOperator(
            task_id="evaluate_model",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="data_science",
            node_name="evaluate_model_node",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
            doc_md="""
            ### Evaluate Model
            
            Evaluates model performance:
            - Calculates R², MAE, RMSE
            - Logs metrics
            - Validates model quality
            
            **Inputs**: regressor, X_test, y_test
            **Output**: Metrics logged
            """,
            sla=timedelta(minutes=10),
        )

        # Dependencies within data science
        split_data >> train_model >> evaluate_model

    # =====================================================
    # REPORTING STAGE
    # =====================================================
    with TaskGroup("reporting", tooltip="Generate visualizations and reports") as reporting:
        
        plot_capacity_express = KedroOperator(
            task_id="plot_passenger_capacity_express",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="reporting",
            node_name="compare_passenger_capacity_exp",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
            doc_md="""
            ### Passenger Capacity Plot (Plotly Express)
            
            Creates bar chart of shuttle passenger capacity.
            
            **Input**: `preprocessed_shuttles.parquet`
            **Output**: `shuttle_passenger_capacity_plot_exp.json` (versioned)
            """,
            sla=timedelta(minutes=5),
        )

        plot_capacity_go = KedroOperator(
            task_id="plot_passenger_capacity_go",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="reporting",
            node_name="compare_passenger_capacity_go",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
            doc_md="""
            ### Passenger Capacity Plot (Graph Objects)
            
            Creates bar chart using Plotly Graph Objects.
            
            **Input**: `preprocessed_shuttles.parquet`
            **Output**: `shuttle_passenger_capacity_plot_go.json` (versioned)
            """,
            sla=timedelta(minutes=5),
        )

        confusion_matrix = KedroOperator(
            task_id="create_confusion_matrix",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="reporting",
            node_name="create_confusion_matrix",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
            doc_md="""
            ### Confusion Matrix
            
            Creates confusion matrix visualization.
            
            **Output**: `dummy_confusion_matrix.png` (versioned)
            """,
            sla=timedelta(minutes=5),
        )

        # All reporting tasks can run in parallel
        [plot_capacity_express, plot_capacity_go, confusion_matrix]

    # =====================================================
    # PIPELINE FLOW
    # =====================================================
    start >> data_processing >> data_science >> reporting >> end

