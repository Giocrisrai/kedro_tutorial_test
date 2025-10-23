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
from typing import Dict, Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

def validate_imports() -> bool:
    """Validate that all required imports work correctly."""
    print("🔍 Validating imports...")
    
    try:
        # Test basic imports
        import pandas as pd
        import numpy as np
        import sklearn
        import joblib
        print("✅ Basic ML libraries imported successfully")
        
        # Test Kedro imports
        from kedro.pipeline import Pipeline, Node
        from kedro.framework.project import find_pipelines
        print("✅ Kedro imports successful")
        
        # Test advanced ML pipeline imports
        from spaceflights.pipelines.advanced_ml.nodes import (
            prepare_regression_data,
            prepare_classification_data,
            train_regression_models,
            train_classification_models,
            evaluate_regression_models,
            evaluate_classification_models,
            save_models_with_dvc,
            create_model_comparison_report
        )
        print("✅ Advanced ML pipeline imports successful")
        
        # Test Airflow imports
        from airflow import DAG
        from airflow.providers.standard.operators.empty import EmptyOperator
        from airflow.sdk import TaskGroup
        print("✅ Airflow imports successful")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during imports: {e}")
        return False

def validate_pipeline_structure() -> bool:
    """Validate the pipeline structure and dependencies."""
    print("🔍 Validating pipeline structure...")
    
    try:
        from spaceflights.pipeline_registry import register_pipelines
        
        pipelines = register_pipelines()
        
        # Check if advanced_ml pipeline exists
        if "advanced_ml" not in pipelines:
            print("❌ advanced_ml pipeline not found in registry")
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
            "create_model_comparison_report_node"
        ]
        
        node_names = [node.name for node in nodes]
        missing_nodes = set(expected_nodes) - set(node_names)
        
        if missing_nodes:
            print(f"❌ Missing nodes: {missing_nodes}")
            return False
        
        print(f"✅ Pipeline structure valid with {len(nodes)} nodes")
        return True
        
    except Exception as e:
        print(f"❌ Pipeline structure validation failed: {e}")
        traceback.print_exc()
        return False

def validate_configuration() -> bool:
    """Validate configuration files."""
    print("🔍 Validating configuration...")
    
    try:
        import yaml
        
        # Check parameters file
        params_file = project_root / "conf" / "base" / "parameters_data_science.yml"
        if not params_file.exists():
            print("❌ parameters_data_science.yml not found")
            return False
        
        with open(params_file, 'r') as f:
            params = yaml.safe_load(f)
        
        # Check advanced_ml parameters
        if "advanced_ml" not in params:
            print("❌ advanced_ml parameters not found")
            return False
        
        advanced_params = params["advanced_ml"]
        required_params = ["test_size", "random_state", "cv_folds", "features", "model_output_path"]
        
        for param in required_params:
            if param not in advanced_params:
                print(f"❌ Missing parameter: {param}")
                return False
        
        print("✅ Configuration validation successful")
        return True
        
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        return False

def validate_airflow_dag() -> bool:
    """Validate Airflow DAG structure."""
    print("🔍 Validating Airflow DAG...")
    
    try:
        # Import the DAG module
        dag_file = project_root / "dags" / "spaceflights_advanced_ml_pipeline.py"
        if not dag_file.exists():
            print("❌ Advanced ML DAG file not found")
            return False
        
        # Try to compile the DAG file
        with open(dag_file, 'r') as f:
            dag_code = f.read()
        
        # Basic syntax check
        compile(dag_code, str(dag_file), 'exec')
        print("✅ Airflow DAG syntax valid")
        
        return True
        
    except SyntaxError as e:
        print(f"❌ Airflow DAG syntax error: {e}")
        return False
    except Exception as e:
        print(f"❌ Airflow DAG validation failed: {e}")
        return False

def validate_data_preparation() -> bool:
    """Validate data preparation functions with sample data."""
    print("🔍 Validating data preparation functions...")
    
    try:
        import pandas as pd
        import numpy as np
        from spaceflights.pipelines.advanced_ml.nodes import (
            prepare_regression_data,
            prepare_classification_data
        )
        
        # Create sample data
        sample_data = pd.DataFrame({
            'engines': [1, 2, 3, 4, 5],
            'passenger_capacity': [10, 20, 30, 40, 50],
            'crew': [2, 3, 4, 5, 6],
            'd_check_complete': [True, False, True, True, False],
            'moon_clearance_complete': [True, True, False, True, True],
            'iata_approved': [True, False, True, True, False],
            'company_rating': [4.5, 3.2, 4.8, 4.1, 3.9],
            'review_scores_rating': [4.2, 3.5, 4.7, 4.0, 3.8],
            'price': [100, 200, 300, 400, 500]
        })
        
        parameters = {
            'features': ['engines', 'passenger_capacity', 'crew', 'd_check_complete', 
                        'moon_clearance_complete', 'iata_approved', 'company_rating', 'review_scores_rating'],
            'test_size': 0.2,
            'random_state': 42,
            'cv_folds': 5
        }
        
        # Test regression data preparation
        X_reg, y_reg = prepare_regression_data(sample_data, parameters)
        if X_reg.shape[0] != 5 or X_reg.shape[1] != 8:
            print("❌ Regression data preparation failed")
            return False
        
        # Test classification data preparation
        X_clf, y_clf, label_encoder = prepare_classification_data(sample_data, parameters)
        if X_clf.shape[0] != 5 or X_clf.shape[1] != 8:
            print("❌ Classification data preparation failed")
            return False
        
        print("✅ Data preparation functions working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Data preparation validation failed: {e}")
        traceback.print_exc()
        return False

def validate_dvc_setup() -> bool:
    """Validate DVC setup and configuration."""
    print("🔍 Validating DVC setup...")
    
    try:
        # Check if dvc.yaml exists
        dvc_file = project_root / "dvc.yaml"
        if not dvc_file.exists():
            print("❌ dvc.yaml not found")
            return False
        
        # Check if .dvc directory exists (indicates DVC is initialized)
        dvc_dir = project_root / ".dvc"
        if not dvc_dir.exists():
            print("⚠️  DVC not initialized (run 'dvc init' to initialize)")
            return False
        
        print("✅ DVC setup validation successful")
        return True
        
    except Exception as e:
        print(f"❌ DVC validation failed: {e}")
        return False

def run_validation_tests() -> Dict[str, bool]:
    """Run all validation tests."""
    print("🚀 Starting Advanced ML Pipeline Validation")
    print("=" * 50)
    
    tests = {
        "imports": validate_imports,
        "pipeline_structure": validate_pipeline_structure,
        "configuration": validate_configuration,
        "airflow_dag": validate_airflow_dag,
        "data_preparation": validate_data_preparation,
        "dvc_setup": validate_dvc_setup
    }
    
    results = {}
    
    for test_name, test_func in tests.items():
        print(f"\n📋 Running {test_name} test...")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results[test_name] = False
    
    return results

def print_summary(results: Dict[str, bool]) -> None:
    """Print validation summary."""
    print("\n" + "=" * 50)
    print("📊 VALIDATION SUMMARY")
    print("=" * 50)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✅ PASS" if passed_test else "❌ FAIL"
        print(f"{test_name:20} {status}")
    
    print("-" * 50)
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All validations passed! The Advanced ML Pipeline is ready to use.")
    else:
        print("⚠️  Some validations failed. Please fix the issues before proceeding.")
    
    return passed == total

def main():
    """Main validation function."""
    try:
        results = run_validation_tests()
        success = print_summary(results)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Validation script failed: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

