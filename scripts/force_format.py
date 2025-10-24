#!/usr/bin/env python3
"""
Script para forzar el formateo de todos los archivos
"""

import os
import subprocess
import sys


def force_format():
    """Fuerza el formateo de todos los archivos"""
    # Cambiar al directorio del proyecto
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_dir)

    print("🔧 Forzando formateo de todos los archivos...")

    # Formatear todos los archivos
    result = subprocess.run(
        ["python3", "-m", "ruff", "format", "src/", "tests/", "dags/", "scripts/"],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        print("✅ Formateo completado exitosamente")
        if result.stdout:
            print(result.stdout)
    else:
        print("❌ Error en el formateo:")
        if result.stderr:
            print(result.stderr)
        return 1

    # Verificar que no queden errores de formateo
    result = subprocess.run(
        [
            "python3",
            "-m",
            "ruff",
            "format",
            "--check",
            "src/",
            "tests/",
            "dags/",
            "scripts/",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        print("✅ Todos los archivos están correctamente formateados")
        return 0
    else:
        print("⚠️ Algunos archivos aún necesitan formateo:")
        if result.stdout:
            print(result.stdout)
        return 1


if __name__ == "__main__":
    sys.exit(force_format())
