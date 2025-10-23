#!/bin/bash
# Installation script for Advanced ML Pipeline dependencies

set -e

echo "🚀 Installing Advanced ML Pipeline Dependencies"
echo "=============================================="

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: pyproject.toml not found. Please run this script from the project root."
    exit 1
fi

# Check Python version
echo "🔍 Checking Python version..."
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python $required_version or higher is required. Found: $python_version"
    exit 1
fi

echo "✅ Python version check passed: $python_version"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
if command -v pip &> /dev/null; then
    pip install -e .
else
    echo "❌ Error: pip not found. Please install pip first."
    exit 1
fi

echo "✅ Python dependencies installed"

# Install additional ML dependencies
echo "📦 Installing additional ML dependencies..."
pip install dvc[s3] joblib numpy pandas matplotlib plotly

echo "✅ Additional ML dependencies installed"

# Initialize DVC if not already initialized
echo "🔧 Setting up DVC..."
if [ ! -d ".dvc" ]; then
    echo "Initializing DVC..."
    dvc init
    echo "✅ DVC initialized"
else
    echo "✅ DVC already initialized"
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p data/05_model_input
mkdir -p data/06_models/advanced_ml/regression
mkdir -p data/06_models/advanced_ml/classification
mkdir -p data/07_model_output
mkdir -p logs

echo "✅ Directories created"

# Validate installation
echo "🔍 Validating installation..."
python3 scripts/validate_advanced_ml.py

echo "🎉 Installation completed successfully!"
echo ""
echo "Next steps:"
echo "1. Run 'kedro run --pipeline advanced_ml' to test the pipeline"
echo "2. Run 'airflow dags list' to verify the DAG is loaded"
echo "3. Use 'dvc add data/06_models/advanced_ml/' to track models with DVC"

