import logging

import pandas as pd
import pytest
from kedro.io import DataCatalog
from kedro.runner import SequentialRunner

from spaceflights.pipelines.data_science import create_pipeline as create_ds_pipeline
from spaceflights.pipelines.data_science.nodes import split_data


@pytest.fixture
def dummy_data():
    return pd.DataFrame(
        {
            "engines": [1, 2, 3],
            "crew": [4, 5, 6],
            "passenger_capacity": [5, 6, 7],
            "price": [120, 290, 30],
            "d_check_complete": [True, False, True],
            "moon_clearance_complete": [False, True, True],
            "iata_approved": [True, True, False],
            "company_rating": [0.8, 0.9, 0.7],
            "review_scores_rating": [4.5, 4.8, 4.2],
        }
    )


@pytest.fixture
def dummy_parameters():
    parameters = {
        "model_options": {
            "test_size": 0.2,
            "random_state": 3,
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
    }
    return parameters


def test_split_data(dummy_data, dummy_parameters):
    X_train, X_test, y_train, y_test = split_data(
        dummy_data, dummy_parameters["model_options"]
    )
    assert len(X_train) == 2
    assert len(y_train) == 2
    assert len(X_test) == 1
    assert len(y_test) == 1


def test_split_data_missing_price(dummy_data, dummy_parameters):
    dummy_data_missing_price = dummy_data.drop(columns="price")
    with pytest.raises(KeyError) as e_info:
        X_train, X_test, y_train, y_test = split_data(
            dummy_data_missing_price, dummy_parameters["model_options"]
        )

    assert "price" in str(e_info.value)


def test_data_science_pipeline(caplog, dummy_data, dummy_parameters):
    pipeline = (
        create_ds_pipeline()
        .from_nodes("split_data_node")
        .to_nodes("evaluate_model_node")
    )
    catalog = DataCatalog()
    catalog["model_input_table"] = dummy_data
    catalog["params:model_options"] = dummy_parameters["model_options"]

    caplog.set_level(logging.INFO, logger="spaceflights.pipelines.data_science.nodes")

    # Run the pipeline
    SequentialRunner().run(pipeline, catalog)

    # Check that the model evaluation logged something
    assert "Model has a coefficient R^2 of" in caplog.text


def test_train_model(dummy_data, dummy_parameters):
    """Test that the train_model function works correctly."""
    from spaceflights.pipelines.data_science.nodes import train_model

    # Create training data
    X_train = dummy_data[dummy_parameters["model_options"]["features"]]
    y_train = dummy_data["price"]

    # Train model
    model = train_model(X_train, y_train)

    # Check that model was created
    assert model is not None
    assert hasattr(model, "predict")
    assert hasattr(model, "fit")


def test_evaluate_model(dummy_data, dummy_parameters):
    """Test that the evaluate_model function works correctly."""
    from spaceflights.pipelines.data_science.nodes import evaluate_model, train_model

    # Create training and test data
    X_train = dummy_data[dummy_parameters["model_options"]["features"]]
    y_train = dummy_data["price"]
    X_test = dummy_data[dummy_parameters["model_options"]["features"]]
    y_test = dummy_data["price"]

    # Train model
    model = train_model(X_train, y_train)

    # Evaluate model
    metrics = evaluate_model(model, X_test, y_test)

    # Check that metrics were returned
    assert isinstance(metrics, dict)
    assert "r2_score" in metrics
    assert "mae" in metrics
    assert "max_error" in metrics
    assert isinstance(metrics["r2_score"], (int, float))
    assert isinstance(metrics["mae"], (int, float))
    assert isinstance(metrics["max_error"], (int, float))
