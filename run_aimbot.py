"""
Main entry point for Blockade 3D Classic Aimbot
Run this file to start the aimbot with GUI
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("=" * 50)
    print("Blockade 3D Classic Aimbot")
    print("=" * 50)
    print("\nStarting aimbot...")
    print("Press INSERT to show/hide the UI")
    print("Right-click while aimbot is enabled to lock on to target")
    print("Press N to stop the script\n")
    
    # Import and run main script
    try:
        import main_074_3_6_5
        # The main script will run its loop
    except ImportError:
        # Try alternative import
        import importlib.util
        spec = importlib.util.spec_from_file_location("main", "main_074_3.6.5.py")
        main = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(main)

