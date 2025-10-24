#!/usr/bin/env python3
"""
Validation script for Advanced ML Pipeline
Validates all components of the advanced ML pipeline including:
- Pipeline structure and dependencies
- Airflow DAG validation
- Configuration validation
- Basic functionality tests
"""

import sys
import traceback
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))


def validate_imports() -> bool:
    """Validate that all required imports work correctly."""

    try:
        # Test basic imports
        import joblib
        import numpy as np
        import pandas as pd
        import sklearn

        # Test Airflow imports
        from airflow import DAG
        from airflow.providers.standard.operators.empty import EmptyOperator
        from airflow.sdk import TaskGroup

        # Test Kedro imports
        from kedro.framework.project import find_pipelines
        from kedro.pipeline import Node, Pipeline

        # Test advanced ML pipeline imports
        from spaceflights.pipelines.advanced_ml.nodes import (
            create_model_comparison_report,
            evaluate_classification_models,
            evaluate_regression_models,
            prepare_classification_data,
            prepare_regression_data,
            save_models_with_dvc,
            train_classification_models,
            train_regression_models,
        )


        return True

    except ImportError:
        return False
    except Exception:
        return False


def validate_pipeline_structure() -> bool:
    """Validate the pipeline structure and dependencies."""

    try:
        from spaceflights.pipeline_registry import register_pipelines

        pipelines = register_pipelines()

        # Check if advanced_ml pipeline exists
        if "advanced_ml" not in pipelines:
            return False

        advanced_ml_pipeline = pipelines["advanced_ml"]

        # Check pipeline nodes
        nodes = advanced_ml_pipeline.nodes
        expected_nodes = [
            "prepare_regression_data_node",
            "prepare_classification_data_node",
            "split_regression_data_node",
            "split_classification_data_node",
            "scale_regression_features_node",
            "scale_classification_features_node",
            "train_regression_models_node",
            "train_classification_models_node",
            "evaluate_regression_models_node",
            "evaluate_classification_models_node",
            "save_regression_models_node",
            "save_classification_models_node",
            "create_model_comparison_report_node",
        ]

        node_names = [node.name for node in nodes]
        missing_nodes = set(expected_nodes) - set(node_names)

        if missing_nodes:
            return False

        return True

    except Exception:
        traceback.print_exc()
        return False


def validate_configuration() -> bool:
    """Validate configuration files."""

    try:
        import yaml

        # Check parameters file
        params_file = project_root / "conf" / "base" / "parameters_data_science.yml"
        if not params_file.exists():
            return False

        with open(params_file) as f:
            params = yaml.safe_load(f)

        # Check advanced_ml parameters
        if "advanced_ml" not in params:
            return False

        advanced_params = params["advanced_ml"]
        required_params = [
            "test_size",
            "random_state",
            "cv_folds",
            "features",
            "model_output_path",
        ]

        for param in required_params:
            if param not in advanced_params:
                return False

        return True

    except Exception:
        return False


def validate_airflow_dag() -> bool:
    """Validate Airflow DAG structure."""

    try:
        # Import the DAG module
        dag_file = project_root / "dags" / "spaceflights_advanced_ml_pipeline.py"
        if not dag_file.exists():
            return False

        # Try to compile the DAG file
        with open(dag_file) as f:
            dag_code = f.read()

        # Basic syntax check
        compile(dag_code, str(dag_file), "exec")

        return True

    except SyntaxError:
        return False
    except Exception:
        return False


def validate_data_preparation() -> bool:
    """Validate data preparation functions with sample data."""

    try:
        import pandas as pd

        from spaceflights.pipelines.advanced_ml.nodes import (
            prepare_classification_data,
            prepare_regression_data,
        )

        # Create sample data
        sample_data = pd.DataFrame(
            {
                "engines": [1, 2, 3, 4, 5],
                "passenger_capacity": [10, 20, 30, 40, 50],
                "crew": [2, 3, 4, 5, 6],
                "d_check_complete": [True, False, True, True, False],
                "moon_clearance_complete": [True, True, False, True, True],
                "iata_approved": [True, False, True, True, False],
                "company_rating": [4.5, 3.2, 4.8, 4.1, 3.9],
                "review_scores_rating": [4.2, 3.5, 4.7, 4.0, 3.8],
                "price": [100, 200, 300, 400, 500],
            }
        )

        parameters = {
            "features": [
                "engines",
                "passenger_capacity",
                "crew",
                "d_check_complete",
                "moon_clearance_complete",
                "iata_approved",
                "company_rating",
                "review_scores_rating",
            ],
            "test_size": 0.2,
            "random_state": 42,
            "cv_folds": 5,
        }

        # Test regression data preparation
        X_reg, y_reg = prepare_regression_data(sample_data, parameters)
        if X_reg.shape[0] != 5 or X_reg.shape[1] != 8:
            return False

        # Test classification data preparation
        X_clf, y_clf, label_encoder = prepare_classification_data(
            sample_data, parameters
        )
        if X_clf.shape[0] != 5 or X_clf.shape[1] != 8:
            return False

        return True

    except Exception:
        traceback.print_exc()
        return False


def validate_dvc_setup() -> bool:
    """Validate DVC setup and configuration."""

    try:
        # Check if dvc.yaml exists
        dvc_file = project_root / "dvc.yaml"
        if not dvc_file.exists():
            return False

        # Check if .dvc directory exists (indicates DVC is initialized)
        dvc_dir = project_root / ".dvc"
        if not dvc_dir.exists():
            return False

        return True

    except Exception:
        return False


def run_validation_tests() -> dict[str, bool]:
    """Run all validation tests."""

    tests = {
        "imports": validate_imports,
        "pipeline_structure": validate_pipeline_structure,
        "configuration": validate_configuration,
        "airflow_dag": validate_airflow_dag,
        "data_preparation": validate_data_preparation,
        "dvc_setup": validate_dvc_setup,
    }

    results = {}

    for test_name, test_func in tests.items():
        try:
            results[test_name] = test_func()
        except Exception:
            results[test_name] = False

    return results


def print_summary(results: dict[str, bool]) -> None:
    """Print validation summary."""

    passed = sum(results.values())
    total = len(results)

    for test_name, passed_test in results.items():
        pass


    if passed == total:
        pass
    else:
        pass

    return passed == total


def main():
    """Main validation function."""
    try:
        results = run_validation_tests()
        success = print_summary(results)
        sys.exit(0 if success else 1)
    except Exception:
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
