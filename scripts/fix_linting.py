#!/usr/bin/env python3
"""
Script para corregir automáticamente errores de linting con ruff
"""

import os
import subprocess
import sys


def run_command(cmd, description):
    """Ejecuta un comando y muestra el resultado"""
    try:
        result = subprocess.run(
            cmd, check=False, shell=True, capture_output=True, text=True
        )
        if result.returncode == 0:
            if result.stdout:
                pass
        elif result.stderr:
            pass
        return result.returncode == 0
    except Exception:
        return False


def main():
    """Función principal para corregir errores de linting"""

    # Cambiar al directorio del proyecto
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_dir)

    # 1. Formatear código automáticamente
    success1 = run_command(
        "python3 -m ruff format src/ tests/ dags/ scripts/",
        "Formatear código automáticamente",
    )

    # 2. Corregir errores automáticamente
    success2 = run_command(
        "python3 -m ruff check src/ tests/ dags/ scripts/ --fix",
        "Corregir errores automáticamente",
    )

    # 3. Verificar que no queden errores
    success3 = run_command(
        "python3 -m ruff check src/ tests/ dags/ scripts/ --output-format=github",
        "Verificar que no queden errores",
    )

    # Resumen

    if success1 and success2 and success3:
        pass
    else:
        pass

    return 0 if (success1 and success2 and success3) else 1


if __name__ == "__main__":
    sys.exit(main())
