"""Advanced ML pipeline with cross-validation, grid search, and DVC integration."""

from kedro.pipeline import Node, Pipeline

from .nodes import (
    create_model_comparison_report,
    evaluate_classification_models,
    evaluate_regression_models,
    prepare_classification_data,
    prepare_regression_data,
    save_models_with_dvc,
    scale_features,
    split_data_with_cv,
    train_classification_models,
    train_regression_models,
)


def create_pipeline(**kwargs) -> Pipeline:
    """Create the advanced ML pipeline.

    Returns:
        Kedro Pipeline object
    """
    return Pipeline(
        [
            # Data preparation nodes
            Node(
                func=prepare_regression_data,
                inputs=["model_input_table", "params:advanced_ml"],
                outputs=["X_reg", "y_reg"],
                name="prepare_regression_data_node",
                tags=["data_preparation", "regression"],
            ),
            Node(
                func=prepare_classification_data,
                inputs=["model_input_table", "params:advanced_ml"],
                outputs=["X_clf", "y_clf", "label_encoder"],
                name="prepare_classification_data_node",
                tags=["data_preparation", "classification"],
            ),
            # Data splitting and scaling
            Node(
                func=split_data_with_cv,
                inputs=["X_reg", "y_reg", "params:advanced_ml"],
                outputs=[
                    "X_reg_train",
                    "X_reg_test",
                    "y_reg_train",
                    "y_reg_test",
                    "cv_splitter_reg",
                ],
                name="split_regression_data_node",
                tags=["data_splitting", "regression"],
            ),
            Node(
                func=split_data_with_cv,
                inputs=["X_clf", "y_clf", "params:advanced_ml"],
                outputs=[
                    "X_clf_train",
                    "X_clf_test",
                    "y_clf_train",
                    "y_clf_test",
                    "cv_splitter_clf",
                ],
                name="split_classification_data_node",
                tags=["data_splitting", "classification"],
            ),
            # Feature scaling
            Node(
                func=scale_features,
                inputs=["X_reg_train", "X_reg_test"],
                outputs=["X_reg_train_scaled", "X_reg_test_scaled", "scaler_reg"],
                name="scale_regression_features_node",
                tags=["feature_scaling", "regression"],
            ),
            Node(
                func=scale_features,
                inputs=["X_clf_train", "X_clf_test"],
                outputs=["X_clf_train_scaled", "X_clf_test_scaled", "scaler_clf"],
                name="scale_classification_features_node",
                tags=["feature_scaling", "classification"],
            ),
            # Model training
            Node(
                func=train_regression_models,
                inputs=[
                    "X_reg_train_scaled",
                    "y_reg_train",
                    "cv_splitter_reg",
                    "params:advanced_ml",
                ],
                outputs="regression_models",
                name="train_regression_models_node",
                tags=["model_training", "regression", "grid_search"],
            ),
            Node(
                func=train_classification_models,
                inputs=[
                    "X_clf_train_scaled",
                    "y_clf_train",
                    "cv_splitter_clf",
                    "params:advanced_ml",
                ],
                outputs="classification_models",
                name="train_classification_models_node",
                tags=["model_training", "classification", "grid_search"],
            ),
            # Model evaluation
            Node(
                func=evaluate_regression_models,
                inputs=["regression_models", "X_reg_test_scaled", "y_reg_test"],
                outputs="regression_evaluation",
                name="evaluate_regression_models_node",
                tags=["model_evaluation", "regression"],
            ),
            Node(
                func=evaluate_classification_models,
                inputs=[
                    "classification_models",
                    "X_clf_test_scaled",
                    "y_clf_test",
                    "label_encoder",
                ],
                outputs="classification_evaluation",
                name="evaluate_classification_models_node",
                tags=["model_evaluation", "classification"],
            ),
            # Model saving with DVC
            Node(
                func=lambda models, params: save_models_with_dvc(
                    models, "regression", params
                ),
                inputs=["regression_models", "params:advanced_ml"],
                outputs="regression_dvc_paths",
                name="save_regression_models_node",
                tags=["model_saving", "regression", "dvc"],
            ),
            Node(
                func=lambda models, params: save_models_with_dvc(
                    models, "classification", params
                ),
                inputs=["classification_models", "params:advanced_ml"],
                outputs="classification_dvc_paths",
                name="save_classification_models_node",
                tags=["model_saving", "classification", "dvc"],
            ),
            # Report generation
            Node(
                func=create_model_comparison_report,
                inputs=[
                    "regression_evaluation",
                    "classification_evaluation",
                    "params:advanced_ml",
                ],
                outputs="model_comparison_report",
                name="create_model_comparison_report_node",
                tags=["reporting", "model_comparison"],
            ),
        ]
    )
