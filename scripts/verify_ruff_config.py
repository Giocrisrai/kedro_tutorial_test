#!/usr/bin/env python3
"""
Script para verificar la configuración de ruff y mostrar información detallada
"""

import os
import subprocess
import sys


def verify_ruff_config():
    """Verifica la configuración de ruff y muestra información detallada"""
    # Cambiar al directorio del proyecto
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_dir)

    print("🔍 Verificando configuración de ruff...")

    # Verificar versión de ruff
    result = subprocess.run(
        ["python3", "-m", "ruff", "--version"], capture_output=True, text=True
    )

    if result.returncode == 0:
        print(f"✅ Versión de ruff: {result.stdout.strip()}")
    else:
        print("❌ Error al obtener versión de ruff")
        if result.stderr:
            print(result.stderr)
        return 1

    # Verificar configuración
    result = subprocess.run(
        ["python3", "-m", "ruff", "check", "--config", ".ruff.toml", "--help"],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        print("✅ Configuración de ruff cargada correctamente")
    else:
        print("❌ Error al cargar configuración de ruff")
        if result.stderr:
            print(result.stderr)
        return 1

    # Verificar formateo con configuración explícita
    result = subprocess.run(
        [
            "python3",
            "-m",
            "ruff",
            "format",
            "--check",
            "--config",
            ".ruff.toml",
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
        if result.stdout:
            print(result.stdout)
    else:
        print("⚠️ Algunos archivos necesitan formateo:")
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(verify_ruff_config())
