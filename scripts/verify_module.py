#!/usr/bin/env python3
"""
Verify that the spaceflights module can be imported correctly
"""

import sys
import os

def verify_module():
    """Verify that the spaceflights module can be imported"""
    print("🔍 Verifying spaceflights module...")
    
    try:
        # Add src to path
        src_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src')
        if src_path not in sys.path:
            sys.path.insert(0, src_path)
        
        # Test spaceflights module
        import spaceflights
        print(f"✅ spaceflights module imported successfully from {spaceflights.__file__}")
        
        # Test pipelines
        from spaceflights.pipelines.data_processing import create_pipeline as create_dp_pipeline
        print("✅ data_processing pipeline imported successfully")
        
        from spaceflights.pipelines.data_science import create_pipeline as create_ds_pipeline
        print("✅ data_science pipeline imported successfully")
        
        from spaceflights.pipelines.reporting import create_pipeline as create_rp_pipeline
        print("✅ reporting pipeline imported successfully")
        
        from spaceflights.pipelines.advanced_ml import create_pipeline as create_aml_pipeline
        print("✅ advanced_ml pipeline imported successfully")
        
        print("\n🎉 All module imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = verify_module()
    sys.exit(0 if success else 1)
