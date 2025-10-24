#!/usr/bin/env python3
"""
Test script to verify that all modules can be imported correctly
"""

import sys
import traceback


def test_imports():
    """Test that all required modules can be imported"""
    print("🔍 Testing module imports...")

    try:
        # Test basic imports
        import pandas as pd

        print("✅ pandas imported successfully")

        import numpy as np

        print("✅ numpy imported successfully")

        import sklearn

        print("✅ sklearn imported successfully")

        import kedro

        print("✅ kedro imported successfully")

        # Test spaceflights module
        from spaceflights.pipelines.data_processing import (
            create_pipeline as create_dp_pipeline,
        )

        print("✅ data_processing pipeline imported successfully")

        from spaceflights.pipelines.data_science import (
            create_pipeline as create_ds_pipeline,
        )

        print("✅ data_science pipeline imported successfully")

        from spaceflights.pipelines.reporting import (
            create_pipeline as create_rp_pipeline,
        )

        print("✅ reporting pipeline imported successfully")

        from spaceflights.pipelines.advanced_ml import (
            create_pipeline as create_aml_pipeline,
        )

        print("✅ advanced_ml pipeline imported successfully")

        print("\n🎉 All imports successful!")
        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False


if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
