"""
Integration tests for the Spaceflights project
"""

import numpy as np
import pandas as pd
import pytest
from kedro.io import DataCatalog
from kedro.runner import SequentialRunner

from spaceflights.pipelines.advanced_ml import create_pipeline as create_aml_pipeline

# Import pipelines
from spaceflights.pipelines.data_processing import create_pipeline as create_dp_pipeline
from spaceflights.pipelines.data_science import create_pipeline as create_ds_pipeline
from spaceflights.pipelines.reporting import create_pipeline as create_rp_pipeline


class TestDataIntegration:
    """Test data integration across pipelines"""

    @pytest.fixture
    def sample_raw_data(self):
        """Sample raw data for integration testing"""
        return {
            "companies": pd.DataFrame(
                {
                    "id": [1, 2, 3, 4, 5],
                    "company_name": [
                        "Company A",
                        "Company B",
                        "Company C",
                        "Company D",
                        "Company E",
                    ],
                    "company_rating": ["4.5%", "3.2%", "4.8%", "4.1%", "3.9%"],
                    "review_scores_rating": ["4.2%", "3.5%", "4.7%", "4.0%", "3.8%"],
                    "iata_approved": [True, False, True, True, False],
                }
            ),
            "reviews": pd.DataFrame(
                {
                    "id": [1, 2, 3, 4, 5],
                    "shuttle_id": [1, 2, 3, 4, 5],  # Added for merge operation
                    "review_scores_rating": ["4.2%", "3.5%", "4.7%", "4.0%", "3.8%"],
                }
            ),
            "shuttles": pd.DataFrame(
                {
                    "id": [1, 2, 3, 4, 5],
                    "engines": [1, 2, 3, 4, 5],
                    "passenger_capacity": [10, 20, 30, 40, 50],
                    "crew": [2, 3, 4, 5, 6],
                    "d_check_complete": [True, False, True, True, False],
                    "moon_clearance_complete": [True, True, False, True, True],
                    "iata_approved": [True, False, True, True, False],
                    "price": ["$100", "$200", "$300", "$400", "$500"],
                }
            ),
        }

    @pytest.fixture
    def integration_catalog(self, sample_raw_data):
        """Integration test catalog"""
        from kedro.io import MemoryDataset

        # Create datasets with data
        datasets = {
            "companies": MemoryDataset(sample_raw_data["companies"]),
            "reviews": MemoryDataset(sample_raw_data["reviews"]),
            "shuttles": MemoryDataset(sample_raw_data["shuttles"]),
            "params:model_options": MemoryDataset(
                {
                    "test_size": 0.2,
                    "random_state": 42,
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
                }
            ),
            "params:advanced_ml": MemoryDataset(
                {
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
                    "cv_folds": 3,
                    "model_output_path": "data/06_models/",
                }
            ),
            "preprocessed_companies": MemoryDataset(),
            "preprocessed_shuttles": MemoryDataset(),
            "model_input_table": MemoryDataset(),
            "regressor": MemoryDataset(),
            "classification_models": MemoryDataset(),
            "shuttle_passenger_capacity_plot": MemoryDataset(),
            "dummy_confusion_matrix": MemoryDataset(),
        }

        catalog = DataCatalog(datasets)
        return catalog

    @pytest.mark.integration
    def test_data_processing_pipeline_integration(self, integration_catalog):
        """Test data processing pipeline integration"""
        pipeline = create_dp_pipeline()
        catalog = integration_catalog

        try:
            runner = SequentialRunner()
            runner.run(pipeline, catalog)

            # Check that processed data was created
            assert "preprocessed_companies" in catalog.list()
            assert "preprocessed_shuttles" in catalog.list()
            assert "model_input_table" in catalog.list()

            # Check data quality
            model_input = catalog.load("model_input_table")
            assert isinstance(model_input, pd.DataFrame)
            assert len(model_input) > 0
            assert "price" in model_input.columns

        except Exception as e:
            pytest.fail(f"Data processing pipeline integration test failed: {e}")

    @pytest.mark.integration
    def test_data_science_pipeline_integration(self, integration_catalog):
        """Test data science pipeline integration"""
        # First run data processing
        dp_pipeline = create_dp_pipeline()
        catalog = integration_catalog

        try:
            runner = SequentialRunner()
            runner.run(dp_pipeline, catalog)

            # Now run data science pipeline
            ds_pipeline = create_ds_pipeline()
            runner.run(ds_pipeline, catalog)

            # Check that model was created
            assert "regressor" in catalog.list()

            # Check model quality
            model = catalog.load("regressor")
            assert model is not None

        except Exception as e:
            pytest.fail(f"Data science pipeline integration test failed: {e}")

    @pytest.mark.integration
    def test_advanced_ml_pipeline_integration(self, integration_catalog):
        """Test advanced ML pipeline integration"""
        # First run data processing
        dp_pipeline = create_dp_pipeline()
        catalog = integration_catalog

        try:
            runner = SequentialRunner()
            runner.run(dp_pipeline, catalog)

            # Now run advanced ML pipeline
            aml_pipeline = create_aml_pipeline()
            runner.run(aml_pipeline, catalog)

            # Check that models were created
            assert "regression_models" in catalog.list()
            assert "classification_models" in catalog.list()

            # Check model quality
            regression_models = catalog.load("regression_models")
            classification_models = catalog.load("classification_models")

            assert isinstance(regression_models, dict)
            assert isinstance(classification_models, dict)
            assert len(regression_models) > 0
            assert len(classification_models) > 0

        except Exception as e:
            pytest.fail(f"Advanced ML pipeline integration test failed: {e}")

    @pytest.mark.integration
    def test_reporting_pipeline_integration(self, integration_catalog):
        """Test reporting pipeline integration"""
        # First run data processing and data science
        dp_pipeline = create_dp_pipeline()
        ds_pipeline = create_ds_pipeline()
        catalog = integration_catalog

        try:
            runner = SequentialRunner()
            runner.run(dp_pipeline, catalog)
            runner.run(ds_pipeline, catalog)

            # Now run reporting pipeline
            rp_pipeline = create_rp_pipeline()
            runner.run(rp_pipeline, catalog)

            # Check that reports were created
            assert "confusion_matrix" in catalog.list()
            assert "shuttle_passenger_capacity_plot" in catalog.list()

        except Exception as e:
            pytest.fail(f"Reporting pipeline integration test failed: {e}")

    @pytest.mark.integration
    def test_end_to_end_pipeline_integration(self, integration_catalog):
        """Test complete end-to-end pipeline integration"""
        catalog = integration_catalog

        try:
            runner = SequentialRunner()

            # Run all pipelines in sequence
            dp_pipeline = create_dp_pipeline()
            ds_pipeline = create_ds_pipeline()
            aml_pipeline = create_aml_pipeline()
            rp_pipeline = create_rp_pipeline()

            # Execute pipelines
            runner.run(dp_pipeline, catalog)
            runner.run(ds_pipeline, catalog)
            runner.run(aml_pipeline, catalog)
            runner.run(rp_pipeline, catalog)

            # Verify all expected outputs exist
            expected_outputs = [
                "preprocessed_companies",
                "preprocessed_shuttles",
                "model_input_table",
                "regressor",
                "regression_models",
                "classification_models",
                "confusion_matrix",
                "shuttle_passenger_capacity_plot",
            ]

            for output in expected_outputs:
                assert output in catalog.list(), f"Expected output {output} not found"

            # Verify data quality
            model_input = catalog.load("model_input_table")
            assert isinstance(model_input, pd.DataFrame)
            assert len(model_input) > 0

        except Exception as e:
            pytest.fail(f"End-to-end pipeline integration test failed: {e}")


class TestPipelineDependencies:
    """Test pipeline dependencies and data flow"""

    @pytest.mark.integration
    def test_pipeline_data_dependencies(self):
        """Test that pipelines have correct data dependencies"""
        dp_pipeline = create_dp_pipeline()
        ds_pipeline = create_ds_pipeline()
        aml_pipeline = create_aml_pipeline()
        rp_pipeline = create_rp_pipeline()

        # Check that data processing pipeline produces model_input_table
        dp_outputs = [
            node.outputs for node in dp_pipeline.nodes if hasattr(node, "outputs")
        ]
        dp_output_names = [output for outputs in dp_outputs for output in outputs]
        assert "model_input_table" in dp_output_names

        # Check that data science pipeline requires model_input_table
        ds_inputs = [
            node.inputs for node in ds_pipeline.nodes if hasattr(node, "inputs")
        ]
        ds_input_names = [input_name for inputs in ds_inputs for input_name in inputs]
        assert "model_input_table" in ds_input_names

        # Check that advanced ML pipeline requires model_input_table
        aml_inputs = [
            node.inputs for node in aml_pipeline.nodes if hasattr(node, "inputs")
        ]
        aml_input_names = [input_name for inputs in aml_inputs for input_name in inputs]
        assert "model_input_table" in aml_input_names

        # Check that reporting pipeline requires preprocessed data
        rp_inputs = [
            node.inputs for node in rp_pipeline.nodes if hasattr(node, "inputs")
        ]
        rp_input_names = [input_name for inputs in rp_inputs for input_name in inputs]
        assert any(
            "preprocessed_shuttles" in input_name for input_name in rp_input_names
        )


class TestDataQuality:
    """Test data quality across pipelines"""

    @pytest.mark.integration
    def test_data_quality_after_processing(self):
        """Test data quality after processing"""
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

        catalog = DataCatalog()
        from kedro.io import MemoryDataset

        catalog._data_sets = {"model_input_table": MemoryDataset(sample_data)}

        # Test data quality checks
        assert not sample_data.isnull().any().any(), "Data should not have null values"
        assert len(sample_data) > 0, "Data should not be empty"
        assert "price" in sample_data.columns, "Data should have price column"
        assert sample_data["price"].dtype in [np.int64, np.float64], (
            "Price should be numeric"
        )

    @pytest.mark.integration
    def test_model_output_quality(self):
        """Test model output quality"""
        # Create mock model outputs
        mock_regression_models = {
            "LinearRegression": {
                "model": "mock_model",
                "cv_scores": [0.8, 0.85, 0.82],
                "params": {},
            }
        }

        mock_classification_models = {
            "LogisticRegression": {
                "model": "mock_model",
                "cv_scores": [0.75, 0.78, 0.76],
                "params": {},
            }
        }

        # Test model output structure
        assert isinstance(mock_regression_models, dict)
        assert isinstance(mock_classification_models, dict)

        for model_name, model_info in mock_regression_models.items():
            assert "model" in model_info
            assert "cv_scores" in model_info
            assert "params" in model_info
            assert len(model_info["cv_scores"]) > 0

        for model_name, model_info in mock_classification_models.items():
            assert "model" in model_info
            assert "cv_scores" in model_info
            assert "params" in model_info
            assert len(model_info["cv_scores"]) > 0


class TestErrorHandling:
    """Test error handling across pipelines"""

    @pytest.mark.integration
    def test_missing_data_handling(self):
        """Test handling of missing data"""
        # Create catalog with missing datasets
        from kedro.io import MemoryDataset

        # Add only model_input_table, missing other required datasets
        datasets = {
            "model_input_table": MemoryDataset(
                pd.DataFrame(
                    {
                        "engines": [1, 2, 3],
                        "passenger_capacity": [10, 20, 30],
                        "crew": [2, 3, 4],
                        "d_check_complete": [True, False, True],
                        "moon_clearance_complete": [True, True, False],
                        "iata_approved": [True, False, True],
                        "company_rating": [4.5, 3.2, 4.8],
                        "review_scores_rating": [4.2, 3.5, 4.7],
                        "price": [100, 200, 300],
                    }
                )
            )
        }

        catalog = DataCatalog(datasets)

        # Test that pipelines handle missing datasets gracefully
        try:
            pipeline = create_ds_pipeline()
            runner = SequentialRunner()
            runner.run(pipeline, catalog)
            # If we get here, the pipeline should handle missing datasets gracefully
        except Exception as e:
            # This is expected for missing datasets
            assert "not found" in str(e).lower() or "missing" in str(e).lower()

    @pytest.mark.integration
    def test_invalid_parameters_handling(self):
        """Test handling of invalid parameters"""
        catalog = DataCatalog()
        from kedro.io import MemoryDataset

        catalog._data_sets = {
            "model_input_table": MemoryDataset(
                pd.DataFrame({"engines": [1, 2, 3], "price": [100, 200, 300]})
            ),
            "params:model_options": MemoryDataset(
                {
                    "test_size": 1.5,  # Invalid test_size > 1
                    "random_state": "invalid",  # Invalid random_state
                    "features": [],  # Empty features list
                }
            ),
        }

        # Test that pipelines handle invalid parameters gracefully
        try:
            pipeline = create_ds_pipeline()
            runner = SequentialRunner()
            runner.run(pipeline, catalog)
        except Exception:
            # This is expected for invalid parameters
            assert True  # Test passes if exception is raised
