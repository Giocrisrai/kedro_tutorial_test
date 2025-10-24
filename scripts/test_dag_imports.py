#!/usr/bin/env python3
"""
Script de prueba para verificar que todos los DAGs se pueden importar correctamente.
Este script simula lo que Airflow hace al cargar DAGs.
"""

import sys
from pathlib import Path

# Agregar el directorio de DAGs al path
dags_dir = Path(__file__).parent.parent / "dags"
sys.path.insert(0, str(dags_dir))


def test_dag_import(dag_file):
    """Intenta importar un archivo DAG y reporta cualquier error."""

    try:
        # Leer el contenido del archivo
        with open(dag_file) as f:
            code = f.read()

        # Intentar compilar el código
        compile(code, dag_file.name, "exec")

        # Intentar importar el módulo
        module_name = dag_file.stem
        if module_name in sys.modules:
            del sys.modules[module_name]

        # Ejecutar el código en un namespace limpio
        namespace = {
            "__file__": str(dag_file),
            "__name__": module_name,
        }
        exec(code, namespace)

        # Verificar que se creó un DAG
        dags_found = []
        for name, obj in namespace.items():
            if hasattr(obj, "dag_id"):
                dags_found.append(obj.dag_id)

        if dags_found:
            return True, None
        else:
            return True, "No DAG object found"

    except SyntaxError as e:
        return False, str(e)
    except Exception as e:
        f"❌ ERROR al importar {dag_file.name}:\n   {type(e).__name__}: {e}"
        return False, str(e)


def main():
    """Función principal que prueba todos los DAGs."""

    # Encontrar todos los archivos .py en el directorio dags
    dag_files = [
        f
        for f in dags_dir.glob("*.py")
        if f.name not in ["__init__.py", "config.py"] and not f.name.endswith(".backup")
    ]

    if not dag_files:
        return 1

    for dag_file in dag_files:
        pass

    # Probar cada DAG
    results = []
    for dag_file in dag_files:
        success, error = test_dag_import(dag_file)
        results.append((dag_file.name, success, error))

    # Resumen de resultados

    total = len(results)
    passed = sum(1 for _, success, _ in results if success)
    failed = total - passed

    if failed > 0:
        for name, success, error in results:
            if not success:
                if error:
                    pass

    if failed == 0:
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
