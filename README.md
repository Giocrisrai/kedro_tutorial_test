# 🚀 Spaceflights - MLOps Project Template

[![Powered by Kedro](https://img.shields.io/badge/powered_by-kedro-ffc900?logo=kedro)](https://kedro.org)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/docker-enabled-blue.svg)](https://www.docker.com/)
[![Airflow](https://img.shields.io/badge/airflow-2.8.0-red.svg)](https://airflow.apache.org/)

> **Professional MLOps project template** integrating Kedro, Docker, Apache Airflow, and best practices for production-ready machine learning systems.

---

## 📋 Overview

Spaceflights is a complete MLOps project demonstrating industry best practices for building, deploying, and maintaining machine learning pipelines. This project serves as a **template and educational resource** for students and practitioners.

### Key Features

- 🔄 **Reproducible Pipelines**: Built with Kedro framework
- 🐳 **Containerized Environments**: Docker for development and production
- ✈️ **Pipeline Orchestration**: Apache Airflow integration
- 📊 **Data Versioning**: Automatic versioning of models and reports
- 🧪 **Testing Framework**: Comprehensive test suite with pytest
- 📈 **Visualization**: Kedro-Viz for pipeline exploration
- 🔧 **Configurable**: Multiple environments (dev, prod)

---

## 🚀 Quick Start

### Prerequisites

- Docker Desktop (20.10+)
- Docker Compose (2.0+)
- 4GB RAM minimum
- 10GB disk space

### Setup (< 5 minutes)

```bash
# 1. Clone repository
git clone <repository-url>
cd spaceflights

# 2. Start development environment
./start.sh development

# 3. Access services
# • JupyterLab: http://localhost:8888
# • Kedro Viz: http://localhost:4141
```

That's it! Your MLOps environment is ready. 🎉

### Run Your First Pipeline

```bash
# Inside container
docker-compose exec jupyter-lab kedro run

# Or specific pipeline
docker-compose exec jupyter-lab kedro run --pipeline data_processing
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **[Setup Guide](./docs/setup.md)** | Detailed installation and configuration |
| **[Architecture](./ARCHITECTURE.md)** | System design and technical decisions |
| **[Docker Guide](./docs/docker.md)** | Docker configuration and usage |
| **[Pipelines](./docs/pipelines.md)** | Pipeline documentation and examples |
| **[Airflow Integration](./docs/airflow.md)** | Orchestration with Airflow |
| **[Troubleshooting](./docs/troubleshooting.md)** | Common issues and solutions |

---

## 🏗️ Project Structure

```
spaceflights/
├── src/spaceflights/        # Source code
│   ├── pipelines/            # Kedro pipelines
│   │   ├── data_processing/  # Data preparation
│   │   ├── data_science/     # Model training
│   │   └── reporting/        # Visualization
│   ├── pipeline_registry.py
│   └── settings.py
├── conf/                     # Configuration files
│   ├── base/                 # Base configuration
│   ├── local/                # Local overrides
│   ├── production/           # Production settings
│   └── airflow/              # Airflow-specific config
├── data/                     # Data layers (gitignored)
│   ├── 01_raw/               # Raw, immutable data
│   ├── 02_intermediate/      # Processed data
│   ├── 03_primary/           # Model inputs
│   ├── 06_models/            # Trained models (versioned)
│   └── 08_reporting/         # Reports (versioned)
├── dags/                     # Airflow DAGs
├── docker/                   # Dockerfiles
├── docs/                     # Documentation
├── notebooks/                # Jupyter notebooks
├── tests/                    # Test suite
└── scripts/                  # Utility scripts
```

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed information.

---

## 🐳 Docker Environments

### Development

Full interactive environment with JupyterLab and visualization:

```bash
./start.sh development
```

**Includes**:
- JupyterLab (port 8888)
- Kedro Viz (port 4141)
- Hot-reload for code changes

### Production

Automated pipeline execution with scheduling:

```bash
./start.sh production
```

**Includes**:
- Automated pipeline runs
- Hourly scheduler
- Kedro Viz for monitoring

### Airflow

Complete Airflow orchestration:

```bash
./start.sh airflow
```

**Includes**:
- Airflow UI (port 8080) - admin/admin
- PostgreSQL metadata store
- Redis for task queue

### Full Stack

All services combined:

```bash
./start.sh all
```

---

## 📊 Pipelines

The project includes three main pipelines:

### 1. Data Processing
Cleans and prepares raw data for modeling.

```bash
docker-compose exec jupyter-lab kedro run --pipeline data_processing
```

**Nodes**: `preprocess_companies`, `preprocess_shuttles`, `create_model_input_table`

### 2. Data Science
Trains and evaluates machine learning models.

```bash
docker-compose exec jupyter-lab kedro run --pipeline data_science
```

**Nodes**: `split_data`, `train_model`, `evaluate_model`

### 3. Reporting
Generates visualizations and reports.

```bash
docker-compose exec jupyter-lab kedro run --pipeline reporting
```

**Nodes**: `create_plots`, `generate_reports`

See [docs/pipelines.md](./docs/pipelines.md) for complete documentation.

---

## 🧪 Testing

```bash
# Run all tests
docker-compose exec jupyter-lab pytest

# With coverage
docker-compose exec jupyter-lab pytest --cov=src/spaceflights

# Specific test file
docker-compose exec jupyter-lab pytest tests/pipelines/data_science/test_pipeline.py
```

---

## 🛠️ Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Pipeline Framework** | Kedro | 1.0.0 |
| **Orchestration** | Apache Airflow | 2.8.0 |
| **Containerization** | Docker | 20.10+ |
| **Language** | Python | 3.11 |
| **Database** | PostgreSQL | 15 (optional) |
| **Cache** | Redis | 7 (optional) |
| **ML Library** | Scikit-learn | 1.5.1 |
| **Visualization** | Plotly | Latest |
| **Testing** | Pytest | 7.2 |

---

## 🎓 For Students

This project demonstrates:

✅ **MLOps Practices**
- Pipeline design and modularity
- Model versioning and tracking
- Environment reproducibility
- Automated orchestration

✅ **Software Engineering**
- Clean code architecture
- Testing and CI/CD
- Configuration management
- Documentation

✅ **DevOps**
- Container orchestration
- Service composition
- Environment management
- Monitoring and logging

### Learning Path

1. **Start Simple**: Run pipelines locally
2. **Understand Docker**: Explore containerization
3. **Learn Kedro**: Build your own pipelines
4. **Integrate Airflow**: Add orchestration
5. **Extend**: Add your own features

---

## 🔧 Development

### Local Development (without Docker)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Run pipeline
kedro run

# Start Kedro Viz
kedro viz run
```

### Adding New Pipelines

```bash
# Create new pipeline
kedro pipeline create my_pipeline

# Implement nodes in src/spaceflights/pipelines/my_pipeline/
# Run new pipeline
kedro run --pipeline my_pipeline
```

See [docs/pipelines.md](./docs/pipelines.md) for details.

---

## 📖 Key Concepts

### Data Catalog
Centralized registry of all data sources and sinks. Define once, use everywhere.

```yaml
# conf/base/catalog.yml
model_input_table:
  type: pandas.ParquetDataset
  filepath: data/03_primary/model_input_table.parquet
```

### Parameters
Configurable pipeline parameters for different environments.

```yaml
# conf/base/parameters_data_science.yml
model_options:
  test_size: 0.2
  random_state: 42
```

### Versioning
Automatic versioning of models and reports for reproducibility.

```yaml
regressor:
  type: pickle.PickleDataset
  filepath: data/06_models/regressor.pickle
  versioned: true  # Creates timestamped versions
```

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file.

---

## 🔗 Resources

- [Kedro Documentation](https://docs.kedro.org/)
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [MLOps Best Practices](https://ml-ops.org/)

---

## 📞 Support

Having issues?

1. Check [docs/troubleshooting.md](./docs/troubleshooting.md)
2. Review [ARCHITECTURE.md](./ARCHITECTURE.md)
3. Search existing issues on GitHub
4. Open a new issue with:
   - Error message
   - Steps to reproduce
   - System information

---

## 🌟 What Makes This Project Special?

✅ **Production-Ready**: Not just a tutorial, a real template  
✅ **Well-Documented**: Extensive documentation for learning  
✅ **Best Practices**: Following industry standards  
✅ **Extensible**: Easy to adapt for your projects  
✅ **Educational**: Designed for learning MLOps  

---

**Built with ❤️ for MLOps education**

*Star ⭐ this repo if you find it useful!*
