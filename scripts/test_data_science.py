#!/usr/bin/env python3
"""
Script de prueba para el pipeline de data science sin pytest.
Verifica que todos los componentes funcionen correctamente.
"""

import sys
from pathlib import Path

import pandas as pd

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_split_data():
    """Prueba la función split_data."""

    try:
        from spaceflights.pipelines.data_science.nodes import split_data

        # Datos de prueba
        dummy_data = pd.DataFrame(
            {
                "engines": [1, 2, 3, 4, 5],
                "crew": [4, 5, 6, 7, 8],
                "passenger_capacity": [5, 6, 7, 8, 9],
                "price": [120, 290, 30, 150, 200],
                "d_check_complete": [True, False, True, True, False],
                "moon_clearance_complete": [False, True, True, False, True],
                "iata_approved": [True, True, False, True, True],
                "company_rating": [0.8, 0.9, 0.7, 0.85, 0.95],
                "review_scores_rating": [4.5, 4.8, 4.2, 4.6, 4.9],
            }
        )

        parameters = {
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

        X_train, X_test, y_train, y_test = split_data(dummy_data, parameters)


        # Verificar que las proporciones son correctas
        total_samples = len(dummy_data)
        expected_train = int(total_samples * 0.8)
        expected_test = total_samples - expected_train

        assert len(X_train) == expected_train, (
            f"Expected {expected_train} train samples, got {len(X_train)}"
        )
        assert len(X_test) == expected_test, (
            f"Expected {expected_test} test samples, got {len(X_test)}"
        )

        return True

    except Exception:
        return False


def test_train_model():
    """Prueba la función train_model."""

    try:
        from spaceflights.pipelines.data_science.nodes import train_model

        # Datos de entrenamiento
        X_train = pd.DataFrame(
            {
                "engines": [1, 2, 3],
                "passenger_capacity": [5, 6, 7],
                "crew": [4, 5, 6],
                "d_check_complete": [True, False, True],
                "moon_clearance_complete": [False, True, True],
                "iata_approved": [True, True, False],
                "company_rating": [0.8, 0.9, 0.7],
                "review_scores_rating": [4.5, 4.8, 4.2],
            }
        )
        y_train = pd.Series([120, 290, 30])

        model = train_model(X_train, y_train)


        # Probar predicción
        model.predict(X_train)

        return True

    except Exception:
        return False


def test_evaluate_model():
    """Prueba la función evaluate_model."""

    try:
        from spaceflights.pipelines.data_science.nodes import (
            evaluate_model,
            train_model,
        )

        # Datos de entrenamiento y prueba
        X_train = pd.DataFrame(
            {
                "engines": [1, 2, 3],
                "passenger_capacity": [5, 6, 7],
                "crew": [4, 5, 6],
                "d_check_complete": [True, False, True],
                "moon_clearance_complete": [False, True, True],
                "iata_approved": [True, True, False],
                "company_rating": [0.8, 0.9, 0.7],
                "review_scores_rating": [4.5, 4.8, 4.2],
            }
        )
        y_train = pd.Series([120, 290, 30])

        X_test = X_train.copy()
        y_test = y_train.copy()

        # Entrenar modelo
        model = train_model(X_train, y_train)

        # Evaluar modelo
        metrics = evaluate_model(model, X_test, y_test)


        # Verificar tipos
        assert isinstance(metrics, dict), "Métricas deben ser un diccionario"
        assert "r2_score" in metrics, "Debe incluir r2_score"
        assert "mae" in metrics, "Debe incluir mae"
        assert "max_error" in metrics, "Debe incluir max_error"

        return True

    except Exception:
        return False


def test_pipeline_import():
    """Prueba que el pipeline se puede importar."""

    try:
        from spaceflights.pipelines.data_science import create_pipeline

        pipeline = create_pipeline()


        # Verificar que tiene los nodos esperados
        node_names = [node.name for node in pipeline.nodes]
        expected_nodes = ["split_data_node", "train_model_node", "evaluate_model_node"]

        for expected_node in expected_nodes:
            assert expected_node in node_names, f"Nodo {expected_node} no encontrado"

        return True

    except Exception:
        return False


def main():
    """Función principal que ejecuta todas las pruebas."""

    tests = [
        ("Importación del Pipeline", test_pipeline_import),
        ("Función split_data", test_split_data),
        ("Función train_model", test_train_model),
        ("Función evaluate_model", test_evaluate_model),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:

        if test_func():
            passed += 1
        else:
            pass


    if passed == total:
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
