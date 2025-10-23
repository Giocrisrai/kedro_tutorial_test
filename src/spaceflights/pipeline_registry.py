"""Project pipelines."""

from kedro.pipeline import Pipeline

from .pipelines import (
    advanced_ml,
    data_processing,
    data_science,
    reporting,
)


def register_pipelines() -> dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    pipelines = {
        "data_processing": data_processing.create_pipeline(),
        "data_science": data_science.create_pipeline(),
        "advanced_ml": advanced_ml.create_pipeline(),
        "reporting": reporting.create_pipeline(),
    }
    
    # Create a comprehensive default pipeline that includes all pipelines
    pipelines["__default__"] = sum(pipelines.values())
    
    # Create a combined ML pipeline (original + advanced)
    pipelines["ml_combined"] = pipelines["data_science"] + pipelines["advanced_ml"]
    
    return pipelines
