#!/usr/bin/env python3
"""
Setup script for spaceflights project
"""

from setuptools import find_packages, setup

setup(
    name="spaceflights",
    version="0.1",
    description="Spaceflights MLOps project",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "kedro>=0.18.0",
        "pandas>=1.5.0",
        "numpy>=1.21.0",
        "scikit-learn>=1.1.0",
        "matplotlib>=3.5.0",
        "seaborn>=0.11.0",
        "plotly>=5.0.0",
        "openpyxl>=3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.8.0",
            "ruff>=0.1.0",
            "mypy>=1.0.0",
        ],
    },
)
