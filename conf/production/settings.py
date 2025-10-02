"""Settings for production environment."""

from conf.base.settings import *

# Production-specific settings
ENVIRONMENT = "production"

# Logging configuration for production
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {
            "format": "%(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "detailed",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": "logs/kedro.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
        },
    },
    "loggers": {
        "kedro": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False,
        },
        "kedro.pipeline": {
            "level": "DEBUG",
            "handlers": ["file"],
            "propagate": False,
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"],
    },
}

# Disable telemetry in production
KEDRO_DISABLE_TELEMETRY = True

# Production data catalog settings
# Use more robust data storage for production
CATALOG = {
    "companies": {
        "type": "pandas.CSVDataset",
        "filepath": "data/01_raw/companies.csv",
        "save_args": {"index": False},
    },
    "shuttles": {
        "type": "pandas.ExcelDataset",
        "filepath": "data/01_raw/shuttles.xlsx",
        "save_args": {"index": False},
    },
    "reviews": {
        "type": "pandas.CSVDataset",
        "filepath": "data/01_raw/reviews.csv",
        "save_args": {"index": False},
    },
    # Use Parquet for better performance in production
    "preprocessed_companies": {
        "type": "pandas.ParquetDataset",
        "filepath": "data/02_intermediate/preprocessed_companies.parquet",
    },
    "preprocessed_shuttles": {
        "type": "pandas.ParquetDataset",
        "filepath": "data/02_intermediate/preprocessed_shuttles.parquet",
    },
    "model_input_table": {
        "type": "pandas.ParquetDataset",
        "filepath": "data/03_primary/model_input_table.parquet",
    },
    "regressor": {
        "type": "pickle.PickleDataset",
        "filepath": "data/06_models/regressor.pickle",
    },
}
