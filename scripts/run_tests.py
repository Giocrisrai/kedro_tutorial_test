#!/usr/bin/env python3
"""
Comprehensive test runner for the Spaceflights project
"""
import subprocess
import sys
import argparse
from pathlib import Path


def run_command(command, description):
    """Run a command and return the result"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print('='*60)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - PASSED")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ {description} - FAILED")
            if result.stderr:
                print("STDERR:", result.stderr)
            if result.stdout:
                print("STDOUT:", result.stdout)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False


def run_unit_tests():
    """Run unit tests"""
    return run_command(
        "python -m pytest tests/pipelines/ -m unit -v --tb=short",
        "Unit Tests"
    )


def run_integration_tests():
    """Run integration tests"""
    return run_command(
        "python -m pytest tests/integration/ -m integration -v --tb=short",
        "Integration Tests"
    )


def run_functional_tests():
    """Run functional tests"""
    return run_command(
        "python -m pytest tests/dags/ -m functional -v --tb=short",
        "Functional Tests"
    )


def run_kedro_tests():
    """Run Kedro-specific tests"""
    return run_command(
        "python -m pytest tests/ -m kedro -v --tb=short",
        "Kedro Tests"
    )


def run_airflow_tests():
    """Run Airflow-specific tests"""
    return run_command(
        "python -m pytest tests/ -m airflow -v --tb=short",
        "Airflow Tests"
    )


def run_all_tests():
    """Run all tests"""
    return run_command(
        "python -m pytest tests/ -v --tb=short --cov=src/spaceflights --cov-report=term-missing",
        "All Tests with Coverage"
    )


def run_linting():
    """Run linting checks"""
    return run_command(
        "python -m ruff check src/ tests/ --fix",
        "Linting Checks"
    )


def run_type_checking():
    """Run type checking"""
    return run_command(
        "python -m mypy src/ --ignore-missing-imports",
        "Type Checking"
    )


def run_docker_tests():
    """Run Docker tests"""
    print(f"\n{'='*60}")
    print("🐳 Docker Tests")
    print('='*60)
    
    # Test Kedro container
    kedro_result = run_command(
        "docker run --rm spaceflights-kedro:test kedro info",
        "Kedro Container Test"
    )
    
    # Test Airflow container
    airflow_result = run_command(
        "docker run --rm spaceflights-airflow:test airflow version",
        "Airflow Container Test"
    )
    
    return kedro_result and airflow_result


def run_validation_scripts():
    """Run validation scripts"""
    print(f"\n{'='*60}")
    print("🔍 Validation Scripts")
    print('='*60)
    
    # Run DAG validation
    dag_result = run_command(
        "python scripts/validate_dag_structure.py",
        "DAG Structure Validation"
    )
    
    # Run Advanced ML validation
    aml_result = run_command(
        "python scripts/validate_advanced_ml.py",
        "Advanced ML Validation"
    )
    
    return dag_result and aml_result


def main():
    """Main test runner"""
    parser = argparse.ArgumentParser(description="Run tests for Spaceflights project")
    parser.add_argument(
        "--type",
        choices=["unit", "integration", "functional", "kedro", "airflow", "all", "docker", "validation"],
        default="all",
        help="Type of tests to run"
    )
    parser.add_argument(
        "--lint",
        action="store_true",
        help="Run linting checks"
    )
    parser.add_argument(
        "--type-check",
        action="store_true",
        help="Run type checking"
    )
    
    args = parser.parse_args()
    
    print("🚀 Spaceflights Test Runner")
    print("=" * 60)
    
    success = True
    
    # Run linting if requested
    if args.lint:
        success &= run_linting()
    
    # Run type checking if requested
    if args.type_check:
        success &= run_type_checking()
    
    # Run tests based on type
    if args.type == "unit":
        success &= run_unit_tests()
    elif args.type == "integration":
        success &= run_integration_tests()
    elif args.type == "functional":
        success &= run_functional_tests()
    elif args.type == "kedro":
        success &= run_kedro_tests()
    elif args.type == "airflow":
        success &= run_airflow_tests()
    elif args.type == "docker":
        success &= run_docker_tests()
    elif args.type == "validation":
        success &= run_validation_scripts()
    elif args.type == "all":
        success &= run_all_tests()
    
    # Print summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print('='*60)
    
    if success:
        print("🎉 All tests passed successfully!")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Please check the output above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
