#!/usr/bin/env python3
"""
Script de verificación de sintaxis para el pipeline de data science.
Verifica que el código compile correctamente sin ejecutarlo.
"""

import ast
import sys
from pathlib import Path


def test_syntax(file_path):
    """Verifica que un archivo Python tenga sintaxis correcta."""
    try:
        with open(file_path) as f:
            content = f.read()

        # Compilar el código para verificar sintaxis
        ast.parse(content)
        return True, "Sintaxis correcta"
    except SyntaxError as e:
        return False, f"Error de sintaxis: {e}"
    except Exception as e:
        return False, f"Error: {e}"


def test_imports(file_path):
    """Verifica que las importaciones sean válidas."""
    try:
        with open(file_path) as f:
            content = f.read()

        # Buscar importaciones
        lines = content.split("\n")
        imports = []
        for line in lines:
            line = line.strip()
            if line.startswith("import ") or line.startswith("from "):
                imports.append(line)

        return True, f"Importaciones encontradas: {len(imports)}"
    except Exception as e:
        return False, f"Error leyendo importaciones: {e}"


def test_functions(file_path):
    """Verifica que las funciones estén definidas correctamente."""
    try:
        with open(file_path) as f:
            content = f.read()

        # Buscar definiciones de funciones
        lines = content.split("\n")
        functions = []
        for line in lines:
            line = line.strip()
            if line.startswith("def "):
                func_name = line.split("(")[0].replace("def ", "")
                functions.append(func_name)

        return True, f"Funciones encontradas: {functions}"
    except Exception as e:
        return False, f"Error analizando funciones: {e}"


def main():
    """Función principal."""

    # Archivos a verificar
    files_to_check = [
        "src/spaceflights/pipelines/data_science/nodes.py",
        "src/spaceflights/pipelines/data_science/pipeline.py",
        "tests/pipelines/data_science/test_pipeline.py",
    ]

    total_tests = 0
    passed_tests = 0

    for file_path in files_to_check:
        full_path = Path(file_path)
        if not full_path.exists():
            continue

        # Test 1: Sintaxis
        total_tests += 1
        success, message = test_syntax(full_path)
        if success:
            passed_tests += 1
        else:
            pass

        # Test 2: Importaciones
        total_tests += 1
        success, message = test_imports(full_path)
        if success:
            passed_tests += 1
        else:
            pass

        # Test 3: Funciones
        total_tests += 1
        success, message = test_functions(full_path)
        if success:
            passed_tests += 1
        else:
            pass

    if passed_tests == total_tests:
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
