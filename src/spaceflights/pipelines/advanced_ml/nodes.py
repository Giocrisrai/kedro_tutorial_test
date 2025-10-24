"""Advanced ML pipeline nodes with cross-validation, grid search, and DVC integration."""

import logging
from pathlib import Path
from typing import Any, Union

# import dvc.api  # DVC integration will be handled separately
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import (
    GridSearchCV,
    KFold,
    cross_val_score,
    train_test_split,
)
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import SVC, SVR

logger = logging.getLogger(__name__)


def prepare_classification_data(
    data: pd.DataFrame, parameters: dict[str, Any]
) -> tuple[pd.DataFrame, pd.Series, LabelEncoder]:
    """Prepare data for classification tasks.

    Args:
        data: Input DataFrame
        parameters: Configuration parameters

    Returns:
        Tuple of (X, y, label_encoder)
    """
    # Create classification target based on price quartiles
    price_quartiles = data["price"].quantile([0.25, 0.5, 0.75])
    data["price_category"] = pd.cut(
        data["price"],
        bins=[
            -np.inf,
            price_quartiles[0.25],
            price_quartiles[0.5],
            price_quartiles[0.75],
            np.inf,
        ],
        labels=["Low", "Medium", "High", "Premium"],
    )

    # Encode categorical target
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(data["price_category"])

    # Select features
    X = data[parameters["features"]]

    logger.info(
        f"Classification data prepared: {X.shape[0]} samples, {X.shape[1]} features"
    )
    logger.info(f"Target distribution: {np.bincount(y)}")

    return X, y, label_encoder


def prepare_regression_data(
    data: pd.DataFrame, parameters: dict[str, Any]
) -> tuple[pd.DataFrame, pd.Series]:
    """Prepare data for regression tasks.

    Args:
        data: Input DataFrame
        parameters: Configuration parameters

    Returns:
        Tuple of (X, y)
    """
    X = data[parameters["features"]]
    y = data["price"]

    logger.info(
        f"Regression data prepared: {X.shape[0]} samples, {X.shape[1]} features"
    )
    logger.info(f"Target range: {y.min():.2f} - {y.max():.2f}")

    return X, y


def split_data_with_cv(
    X: pd.DataFrame, y: Union[pd.Series, np.ndarray], parameters: dict[str, Any]
) -> tuple[
    pd.DataFrame,
    pd.DataFrame,
    Union[pd.Series, np.ndarray],
    Union[pd.Series, np.ndarray],
    KFold,
]:
    """Split data into train/test sets and create cross-validation splitter.

    Args:
        X: Feature matrix
        y: Target vector
        parameters: Configuration parameters

    Returns:
        Tuple of (X_train, X_test, y_train, y_test, cv_splitter)
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=parameters["test_size"],
        random_state=parameters["random_state"],
        stratify=y if parameters.get("stratify", False) else None,
    )

    # Create cross-validation splitter
    cv_splitter = KFold(
        n_splits=parameters["cv_folds"],
        shuffle=True,
        random_state=parameters["random_state"],
    )

    logger.info(f"Data split: {X_train.shape[0]} train, {X_test.shape[0]} test")
    logger.info(f"Cross-validation: {parameters['cv_folds']} folds")

    return X_train, X_test, y_train, y_test, cv_splitter


def scale_features(
    X_train: pd.DataFrame, X_test: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame, StandardScaler]:
    """Scale features using StandardScaler.

    Args:
        X_train: Training features
        X_test: Test features

    Returns:
        Tuple of (X_train_scaled, X_test_scaled, scaler)
    """
    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(
        scaler.fit_transform(X_train), columns=X_train.columns, index=X_train.index
    )
    X_test_scaled = pd.DataFrame(
        scaler.transform(X_test), columns=X_test.columns, index=X_test.index
    )

    logger.info("Features scaled using StandardScaler")
    return X_train_scaled, X_test_scaled, scaler


def train_regression_models(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    cv_splitter: KFold,
    parameters: dict[str, Any],
) -> dict[str, Any]:
    """Train multiple regression models with cross-validation and grid search.

    Args:
        X_train: Training features
        y_train: Training targets
        cv_splitter: Cross-validation splitter
        parameters: Configuration parameters

    Returns:
        Dictionary containing trained models and results
    """
    models = {}
    results = {}

    # Define models and their parameter grids
    model_configs = {
        "ridge": {
            "model": Ridge(),
            "params": {
                "alpha": [0.1, 1.0, 10.0, 100.0],
                "solver": ["auto", "svd", "cholesky", "lsqr", "saga"],
            },
        },
        "random_forest": {
            "model": RandomForestRegressor(random_state=parameters["random_state"]),
            "params": {
                "n_estimators": [50, 100, 200],
                "max_depth": [None, 10, 20, 30],
                "min_samples_split": [2, 5, 10],
            },
        },
        "svr": {
            "model": SVR(),
            "params": {
                "C": [0.1, 1.0, 10.0],
                "gamma": ["scale", "auto", 0.001, 0.01, 0.1],
                "kernel": ["rbf", "linear", "poly"],
            },
        },
    }

    for model_name, config in model_configs.items():
        logger.info(f"Training {model_name} regression model...")

        # Grid search with cross-validation
        grid_search = GridSearchCV(
            config["model"],
            config["params"],
            cv=cv_splitter,
            scoring="neg_mean_squared_error",
            n_jobs=-1,
            verbose=1,
        )

        grid_search.fit(X_train, y_train)

        # Cross-validation scores
        cv_scores = cross_val_score(
            grid_search.best_estimator_,
            X_train,
            y_train,
            cv=cv_splitter,
            scoring="neg_mean_squared_error",
        )

        models[model_name] = {
            "model": grid_search.best_estimator_,
            "best_params": grid_search.best_params_,
            "best_score": grid_search.best_score_,
            "cv_scores": cv_scores,
            "cv_mean": cv_scores.mean(),
            "cv_std": cv_scores.std(),
        }

        results[model_name] = {
            "best_params": grid_search.best_params_,
            "cv_mean_rmse": np.sqrt(-cv_scores.mean()),
            "cv_std_rmse": np.sqrt(cv_scores.std()),
            "best_cv_score": grid_search.best_score_,
        }

        logger.info(f"{model_name} - Best params: {grid_search.best_params_}")
        logger.info(
            f"{model_name} - CV RMSE: {np.sqrt(-cv_scores.mean()):.4f} ± {np.sqrt(cv_scores.std()):.4f}"
        )

    return {"models": models, "results": results}


def train_classification_models(
    X_train: pd.DataFrame,
    y_train: np.ndarray,
    cv_splitter: KFold,
    parameters: dict[str, Any],
) -> dict[str, Any]:
    """Train multiple classification models with cross-validation and grid search.

    Args:
        X_train: Training features
        y_train: Training targets
        cv_splitter: Cross-validation splitter
        parameters: Configuration parameters

    Returns:
        Dictionary containing trained models and results
    """
    models = {}
    results = {}

    # Define models and their parameter grids
    model_configs = {
        "logistic_regression": {
            "model": LogisticRegression(
                random_state=parameters["random_state"], max_iter=1000
            ),
            "params": {
                "C": [0.1, 1.0, 10.0, 100.0],
                "penalty": ["l1", "l2", "elasticnet"],
                "solver": ["liblinear", "saga"],
            },
        },
        "random_forest": {
            "model": RandomForestClassifier(random_state=parameters["random_state"]),
            "params": {
                "n_estimators": [50, 100, 200],
                "max_depth": [None, 10, 20, 30],
                "min_samples_split": [2, 5, 10],
                "class_weight": ["balanced", None],
            },
        },
        "svc": {
            "model": SVC(random_state=parameters["random_state"], probability=True),
            "params": {
                "C": [0.1, 1.0, 10.0],
                "gamma": ["scale", "auto", 0.001, 0.01, 0.1],
                "kernel": ["rbf", "linear", "poly"],
            },
        },
    }

    for model_name, config in model_configs.items():
        logger.info(f"Training {model_name} classification model...")

        # Grid search with cross-validation
        grid_search = GridSearchCV(
            config["model"],
            config["params"],
            cv=cv_splitter,
            scoring="f1_weighted",
            n_jobs=-1,
            verbose=1,
        )

        grid_search.fit(X_train, y_train)

        # Cross-validation scores
        cv_scores = cross_val_score(
            grid_search.best_estimator_,
            X_train,
            y_train,
            cv=cv_splitter,
            scoring="f1_weighted",
        )

        models[model_name] = {
            "model": grid_search.best_estimator_,
            "best_params": grid_search.best_params_,
            "best_score": grid_search.best_score_,
            "cv_scores": cv_scores,
            "cv_mean": cv_scores.mean(),
            "cv_std": cv_scores.std(),
        }

        results[model_name] = {
            "best_params": grid_search.best_params_,
            "cv_mean_f1": cv_scores.mean(),
            "cv_std_f1": cv_scores.std(),
            "best_cv_score": grid_search.best_score_,
        }

        logger.info(f"{model_name} - Best params: {grid_search.best_params_}")
        logger.info(
            f"{model_name} - CV F1: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}"
        )

    return {"models": models, "results": results}


def evaluate_regression_models(
    models: dict[str, Any], X_test: pd.DataFrame, y_test: pd.Series
) -> dict[str, Any]:
    """Evaluate regression models on test set.

    Args:
        models: Dictionary of trained models
        X_test: Test features
        y_test: Test targets

    Returns:
        Dictionary containing evaluation metrics
    """
    evaluation_results = {}

    for model_name, model_info in models.items():
        model = model_info["model"]
        y_pred = model.predict(X_test)

        metrics = {
            "r2_score": r2_score(y_test, y_pred),
            "mae": mean_absolute_error(y_test, y_pred),
            "mse": mean_squared_error(y_test, y_pred),
            "rmse": np.sqrt(mean_squared_error(y_test, y_pred)),
        }

        evaluation_results[model_name] = metrics

        logger.info(f"{model_name} Test Results:")
        logger.info(f"  R² Score: {metrics['r2_score']:.4f}")
        logger.info(f"  MAE: {metrics['mae']:.4f}")
        logger.info(f"  RMSE: {metrics['rmse']:.4f}")

    return evaluation_results


def evaluate_classification_models(
    models: dict[str, Any],
    X_test: pd.DataFrame,
    y_test: np.ndarray,
    label_encoder: LabelEncoder,
) -> dict[str, Any]:
    """Evaluate classification models on test set.

    Args:
        models: Dictionary of trained models
        X_test: Test features
        y_test: Test targets
        label_encoder: Label encoder for target classes

    Returns:
        Dictionary containing evaluation metrics
    """
    evaluation_results = {}

    for model_name, model_info in models.items():
        model = model_info["model"]
        y_pred = model.predict(X_test)
        y_pred_proba = (
            model.predict_proba(X_test) if hasattr(model, "predict_proba") else None
        )

        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, average="weighted"),
            "recall": recall_score(y_test, y_pred, average="weighted"),
            "f1_score": f1_score(y_test, y_pred, average="weighted"),
            "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
        }

        # Add ROC AUC if probabilities are available
        if y_pred_proba is not None and len(np.unique(y_test)) > 2:
            try:
                metrics["roc_auc"] = roc_auc_score(
                    y_test, y_pred_proba, multi_class="ovr"
                )
            except ValueError:
                metrics["roc_auc"] = None

        evaluation_results[model_name] = metrics

        logger.info(f"{model_name} Test Results:")
        logger.info(f"  Accuracy: {metrics['accuracy']:.4f}")
        logger.info(f"  Precision: {metrics['precision']:.4f}")
        logger.info(f"  Recall: {metrics['recall']:.4f}")
        logger.info(f"  F1 Score: {metrics['f1_score']:.4f}")
        if metrics.get("roc_auc"):
            logger.info(f"  ROC AUC: {metrics['roc_auc']:.4f}")

    return evaluation_results


def save_models_with_dvc(
    models: dict[str, Any], model_type: str, parameters: dict[str, Any]
) -> dict[str, str]:
    """Save models using DVC for version control.

    Args:
        models: Dictionary of trained models
        model_type: Type of models ("regression" or "classification")
        parameters: Configuration parameters

    Returns:
        Dictionary mapping model names to DVC paths
    """
    dvc_paths = {}
    base_path = Path(parameters["model_output_path"]) / model_type

    for model_name, model_info in models.items():
        # Save model using joblib
        model_path = base_path / f"{model_name}_model.pkl"
        model_path.parent.mkdir(parents=True, exist_ok=True)

        joblib.dump(model_info["model"], model_path)

        # Save metadata
        metadata_path = base_path / f"{model_name}_metadata.pkl"
        metadata = {
            "best_params": model_info["best_params"],
            "cv_scores": model_info["cv_scores"],
            "cv_mean": model_info["cv_mean"],
            "cv_std": model_info["cv_std"],
            "model_type": model_type,
            "model_name": model_name,
        }

        joblib.dump(metadata, metadata_path)

        # Add to DVC (paths will be tracked by DVC)
        dvc_paths[model_name] = str(model_path)

        logger.info(f"Saved {model_name} {model_type} model to {model_path}")

    return dvc_paths


def create_model_comparison_report(
    regression_results: dict[str, Any],
    classification_results: dict[str, Any],
    parameters: dict[str, Any],
) -> dict[str, Any]:
    """Create comprehensive model comparison report.

    Args:
        regression_results: Regression model results
        classification_results: Classification model results
        parameters: Configuration parameters

    Returns:
        Dictionary containing comparison report
    """
    report = {
        "timestamp": pd.Timestamp.now().isoformat(),
        "parameters": parameters,
        "regression_models": regression_results,
        "classification_models": classification_results,
        "best_models": {},
    }

    # Find best regression model
    if regression_results:
        best_reg_model = min(regression_results.items(), key=lambda x: x[1]["rmse"])
        report["best_models"]["regression"] = {
            "model": best_reg_model[0],
            "rmse": best_reg_model[1]["rmse"],
            "r2_score": best_reg_model[1]["r2_score"],
        }

    # Find best classification model
    if classification_results:
        best_clf_model = max(
            classification_results.items(), key=lambda x: x[1]["f1_score"]
        )
        report["best_models"]["classification"] = {
            "model": best_clf_model[0],
            "f1_score": best_clf_model[1]["f1_score"],
            "accuracy": best_clf_model[1]["accuracy"],
        }

    # Save report
    report_path = Path(parameters["model_output_path"]) / "model_comparison_report.pkl"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(report, report_path)

    logger.info(f"Model comparison report saved to {report_path}")
    logger.info(
        f"Best regression model: {report['best_models'].get('regression', {}).get('model', 'N/A')}"
    )
    logger.info(
        f"Best classification model: {report['best_models'].get('classification', {}).get('model', 'N/A')}"
    )

    return report
