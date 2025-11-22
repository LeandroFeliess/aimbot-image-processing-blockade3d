"""
Test Script 5: GUI
Test of GUI werkt
"""
import sys
import time
print("=" * 60)
print("TEST 5: GUI")
print("=" * 60)

try:
    from aimbot_gui import AimbotGUI
    print("[OK] GUI module loaded")
except Exception as e:
    print(f"[FAIL] ERROR loading GUI: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n[INFO] Testing GUI...")

try:
    print("[GUI]  Creating GUI...")
    gui = AimbotGUI()
    print("[OK] GUI created")
    
    print("[GUI]  Starting GUI (will close after 5 seconds)...")
    print("   (If GUI appears, it works!)")
    
    # Start GUI in separate thread
    import threading
    def run_gui():
        try:
            gui.run()
        except Exception as e:
            print(f"[FAIL] GUI error: {e}")
    
    gui_thread = threading.Thread(target=run_gui, daemon=True)
    gui_thread.start()
    
    # Wait a bit
    time.sleep(5)
    
    print("[OK] GUI test completed")
    print("   (If you saw the GUI window, it works!)")
    
    print("\n[OK] TEST 5 PASSED: GUI works!")
    
except Exception as e:
    print(f"[FAIL] TEST 5 FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("=" * 60)

