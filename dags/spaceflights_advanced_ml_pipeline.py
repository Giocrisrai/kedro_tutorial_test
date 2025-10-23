"""
Spaceflights Advanced ML Pipeline - Cross-Validation, Grid Search & DVC Integration

This DAG orchestrates the advanced machine learning workflow:
1. Data Processing: Clean and prepare data
2. Advanced ML: Cross-validation, grid search, multiple models
3. Model Evaluation: Comprehensive evaluation metrics
4. DVC Integration: Version control for models
5. Reporting: Model comparison and performance reports

Schedule: Weekly on Sundays at 3 AM UTC
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

# DAG documentation
DAG_DOC_MD = """
# Spaceflights Advanced ML Pipeline

Advanced machine learning workflow with cross-validation, grid search, and DVC integration.

## Pipeline Stages

### 1. Data Processing
- Preprocess company data
- Preprocess shuttle data
- Create model input table

### 2. Advanced ML Pipeline
- **Data Preparation**: Prepare regression and classification datasets
- **Cross-Validation**: 5-fold cross-validation for robust evaluation
- **Grid Search**: Hyperparameter optimization for multiple models
- **Model Training**: Train multiple regression and classification models
- **Model Evaluation**: Comprehensive performance metrics
- **DVC Integration**: Version control for models and results

### 3. Model Comparison & Reporting
- Compare model performance across algorithms
- Generate comprehensive evaluation reports
- Save best models with DVC versioning

## Models Included

### Regression Models
- Ridge Regression
- Random Forest Regressor
- Support Vector Regressor

### Classification Models
- Logistic Regression
- Random Forest Classifier
- Support Vector Classifier

## Features

- **Cross-Validation**: 5-fold CV for robust model evaluation
- **Grid Search**: Automated hyperparameter tuning
- **DVC Integration**: Model versioning and reproducibility
- **Comprehensive Metrics**: R², MAE, RMSE, Accuracy, Precision, Recall, F1
- **Model Comparison**: Automated best model selection

## Schedule

Runs weekly on Sundays at 3:00 AM UTC for comprehensive model retraining.

## SLAs

- Data Processing: 30 minutes
- Advanced ML Training: 2 hours
- Model Evaluation: 30 minutes
- DVC Operations: 15 minutes

## Monitoring

Check Kedro Viz for pipeline visualization: http://localhost:4141
DVC tracking: `dvc metrics show` and `dvc plots show`
"""

# Define the DAG
with DAG(
    dag_id="spaceflights_advanced_ml_pipeline",
    description="Advanced ML pipeline with cross-validation, grid search, and DVC",
    doc_md=DAG_DOC_MD,
    start_date=DAG_START_DATE,
    schedule="0 3 * * 0",  # Weekly on Sundays at 3 AM UTC
    catchup=False,
    max_active_runs=1,  # One run at a time
    default_args=DEFAULT_DAG_ARGS,
    tags=TAGS["ML"] + TAGS["PRODUCTION"] + ["advanced", "cross-validation", "grid-search", "dvc"],
) as dag:

    # Start and end markers
    start = EmptyOperator(
        task_id="start",
        doc_md="Advanced ML pipeline execution start marker",
    )

    end = EmptyOperator(
        task_id="end",
        doc_md="Advanced ML pipeline execution end marker",
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
    # ADVANCED ML PIPELINE STAGE
    # =====================================================
    with TaskGroup("advanced_ml", tooltip="Advanced ML with cross-validation and grid search") as advanced_ml:
        
        # Data preparation
        prepare_regression_data = KedroOperator(
            task_id="prepare_regression_data",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="advanced_ml",
            node_name="prepare_regression_data_node",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
            doc_md="""
            ### Prepare Regression Data
            
            Prepares data for regression tasks:
            - Selects features for regression
            - Creates continuous target variable (price)
            - Handles missing values
            
            **Input**: `model_input_table.parquet`
            **Outputs**: X_reg, y_reg
            """,
            sla=timedelta(minutes=5),
        )

        prepare_classification_data = KedroOperator(
            task_id="prepare_classification_data",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="advanced_ml",
            node_name="prepare_classification_data_node",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
            doc_md="""
            ### Prepare Classification Data
            
            Prepares data for classification tasks:
            - Creates categorical target based on price quartiles
            - Encodes target labels
            - Selects features for classification
            
            **Input**: `model_input_table.parquet`
            **Outputs**: X_clf, y_clf, label_encoder
            """,
            sla=timedelta(minutes=5),
        )

        # Data splitting and scaling
        split_regression_data = KedroOperator(
            task_id="split_regression_data",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="advanced_ml",
            node_name="split_regression_data_node",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
            doc_md="""
            ### Split Regression Data
            
            Splits regression data with cross-validation:
            - Train/test split with stratification
            - Creates 5-fold cross-validation splitter
            - Ensures reproducible splits
            
            **Inputs**: X_reg, y_reg, parameters
            **Outputs**: X_reg_train, X_reg_test, y_reg_train, y_reg_test, cv_splitter_reg
            """,
            sla=timedelta(minutes=5),
        )

        split_classification_data = KedroOperator(
            task_id="split_classification_data",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="advanced_ml",
            node_name="split_classification_data_node",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
            doc_md="""
            ### Split Classification Data
            
            Splits classification data with cross-validation:
            - Train/test split with stratification
            - Creates 5-fold cross-validation splitter
            - Maintains class distribution
            
            **Inputs**: X_clf, y_clf, parameters
            **Outputs**: X_clf_train, X_clf_test, y_clf_train, y_clf_test, cv_splitter_clf
            """,
            sla=timedelta(minutes=5),
        )

        # Feature scaling
        scale_regression_features = KedroOperator(
            task_id="scale_regression_features",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="advanced_ml",
            node_name="scale_regression_features_node",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
            doc_md="""
            ### Scale Regression Features
            
            Scales features for regression models:
            - StandardScaler for consistent feature ranges
            - Fits on training data, transforms test data
            - Preserves feature names and indices
            
            **Inputs**: X_reg_train, X_reg_test
            **Outputs**: X_reg_train_scaled, X_reg_test_scaled, scaler_reg
            """,
            sla=timedelta(minutes=5),
        )

        scale_classification_features = KedroOperator(
            task_id="scale_classification_features",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="advanced_ml",
            node_name="scale_classification_features_node",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
            doc_md="""
            ### Scale Classification Features
            
            Scales features for classification models:
            - StandardScaler for consistent feature ranges
            - Fits on training data, transforms test data
            - Preserves feature names and indices
            
            **Inputs**: X_clf_train, X_clf_test
            **Outputs**: X_clf_train_scaled, X_clf_test_scaled, scaler_clf
            """,
            sla=timedelta(minutes=5),
        )

        # Model training with grid search
        train_regression_models = KedroOperator(
            task_id="train_regression_models",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="advanced_ml",
            node_name="train_regression_models_node",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
            doc_md="""
            ### Train Regression Models
            
            Trains multiple regression models with grid search:
            - Ridge Regression with hyperparameter tuning
            - Random Forest Regressor with grid search
            - Support Vector Regressor with parameter optimization
            - 5-fold cross-validation for each model
            - Comprehensive hyperparameter grids
            
            **Inputs**: X_reg_train_scaled, y_reg_train, cv_splitter_reg, parameters
            **Output**: regression_models (with best parameters and CV scores)
            """,
            sla=timedelta(minutes=90),
        )

        train_classification_models = KedroOperator(
            task_id="train_classification_models",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="advanced_ml",
            node_name="train_classification_models_node",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
            doc_md="""
            ### Train Classification Models
            
            Trains multiple classification models with grid search:
            - Logistic Regression with hyperparameter tuning
            - Random Forest Classifier with grid search
            - Support Vector Classifier with parameter optimization
            - 5-fold cross-validation for each model
            - Comprehensive hyperparameter grids
            
            **Inputs**: X_clf_train_scaled, y_clf_train, cv_splitter_clf, parameters
            **Output**: classification_models (with best parameters and CV scores)
            """,
            sla=timedelta(minutes=90),
        )

        # Model evaluation
        evaluate_regression_models = KedroOperator(
            task_id="evaluate_regression_models",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="advanced_ml",
            node_name="evaluate_regression_models_node",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
            doc_md="""
            ### Evaluate Regression Models
            
            Evaluates regression models on test set:
            - R² Score for model fit quality
            - Mean Absolute Error (MAE)
            - Root Mean Square Error (RMSE)
            - Comprehensive performance comparison
            
            **Inputs**: regression_models, X_reg_test_scaled, y_reg_test
            **Output**: regression_evaluation (metrics for all models)
            """,
            sla=timedelta(minutes=15),
        )

        evaluate_classification_models = KedroOperator(
            task_id="evaluate_classification_models",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="advanced_ml",
            node_name="evaluate_classification_models_node",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
            doc_md="""
            ### Evaluate Classification Models
            
            Evaluates classification models on test set:
            - Accuracy, Precision, Recall, F1-Score
            - Confusion Matrix for detailed analysis
            - ROC AUC Score (multi-class)
            - Comprehensive performance comparison
            
            **Inputs**: classification_models, X_clf_test_scaled, y_clf_test, label_encoder
            **Output**: classification_evaluation (metrics for all models)
            """,
            sla=timedelta(minutes=15),
        )

        # DVC model saving
        save_regression_models = KedroOperator(
            task_id="save_regression_models",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="advanced_ml",
            node_name="save_regression_models_node",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
            doc_md="""
            ### Save Regression Models with DVC
            
            Saves regression models with DVC versioning:
            - Serializes best models using joblib
            - Saves metadata (parameters, CV scores)
            - Integrates with DVC for version control
            - Enables model reproducibility and tracking
            
            **Inputs**: regression_models, parameters
            **Output**: regression_dvc_paths (DVC-tracked model paths)
            """,
            sla=timedelta(minutes=10),
        )

        save_classification_models = KedroOperator(
            task_id="save_classification_models",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="advanced_ml",
            node_name="save_classification_models_node",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
            doc_md="""
            ### Save Classification Models with DVC
            
            Saves classification models with DVC versioning:
            - Serializes best models using joblib
            - Saves metadata (parameters, CV scores)
            - Integrates with DVC for version control
            - Enables model reproducibility and tracking
            
            **Inputs**: classification_models, parameters
            **Output**: classification_dvc_paths (DVC-tracked model paths)
            """,
            sla=timedelta(minutes=10),
        )

        # Report generation
        create_model_comparison_report = KedroOperator(
            task_id="create_model_comparison_report",
            package_name=KEDRO_PACKAGE_NAME,
            pipeline_name="advanced_ml",
            node_name="create_model_comparison_report_node",
            project_path=KEDRO_PROJECT_PATH,
            env=KEDRO_ENV,
            conf_source=KEDRO_CONF_SOURCE,
            doc_md="""
            ### Create Model Comparison Report
            
            Generates comprehensive model comparison report:
            - Compares all regression and classification models
            - Identifies best performing models
            - Creates detailed performance summary
            - Saves report for analysis and tracking
            
            **Inputs**: regression_evaluation, classification_evaluation, parameters
            **Output**: model_comparison_report (comprehensive analysis)
            """,
            sla=timedelta(minutes=10),
        )

        # Dependencies within advanced ML
        prepare_regression_data >> split_regression_data
        prepare_classification_data >> split_classification_data
        split_regression_data >> scale_regression_features >> train_regression_models
        split_classification_data >> scale_classification_features >> train_classification_models
        train_regression_models >> evaluate_regression_models >> save_regression_models
        train_classification_models >> evaluate_classification_models >> save_classification_models
        save_regression_models >> create_model_comparison_report
        save_classification_models >> create_model_comparison_report

    # =====================================================
    # PIPELINE FLOW
    # =====================================================
    start >> data_processing >> advanced_ml >> end

