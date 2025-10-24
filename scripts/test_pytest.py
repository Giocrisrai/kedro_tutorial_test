#!/usr/bin/env python3
"""
Test script to verify that pytest can discover and run tests correctly
"""

import sys
import subprocess
import os

def test_pytest_discovery():
    """Test that pytest can discover tests correctly"""
    print("🔍 Testing pytest discovery...")
    
    try:
        # Test pytest discovery
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/integration/test_integration.py", 
            "--collect-only", "-q"
        ], capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(__file__)))
        
        print(f"Pytest discovery result: {result.returncode}")
        if result.stdout:
            print(f"STDOUT: {result.stdout}")
        if result.stderr:
            print(f"STDERR: {result.stderr}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running pytest: {e}")
        return False

if __name__ == "__main__":
    success = test_pytest_discovery()
    sys.exit(0 if success else 1)
