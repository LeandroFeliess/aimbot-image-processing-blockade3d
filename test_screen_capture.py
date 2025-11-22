"""
Test Script 2: Screen Capture
Test of screen capture werkt
"""
import sys
import cv2
import numpy as np
print("=" * 60)
print("TEST 2: Screen Capture")
print("=" * 60)

try:
    from grabscreen import grab_screen
    from window_finder import window_finder
    import config
    print("[OK] Modules loaded")
except Exception as e:
    print(f"[FAIL] ERROR loading modules: {e}")
    sys.exit(1)

print("\n[INFO] Testing screen capture...")

# Test 1: Window detection
if not window_finder.wait_for_window(timeout=3):
    print("[FAIL] Window not found - cannot test screen capture")
    sys.exit(1)

print("[OK] Window found")

# Test 2: Get game region
game_region = window_finder.get_game_region()
if not game_region:
    print("[FAIL] Could not get game region")
    sys.exit(1)

left, top, width, height = game_region
print(f"[OK] Game region: ({left}, {top}) - {width} x {height}")

# Test 3: Capture screen
try:
    print("[CAPTURE] Capturing screen...")
    screen = grab_screen(region=(left, top, left + width, top + height), use_window_finder=True)
    
    if screen is None:
        print("[FAIL] Screen capture returned None")
        sys.exit(1)
    
    if screen.size == 0:
        print("[FAIL] Screen capture is empty")
        sys.exit(1)
    
    print(f"[OK] Screen captured: {screen.shape} (height x width x channels)")
    print(f"   Data type: {screen.dtype}")
    print(f"   Min value: {screen.min()}, Max value: {screen.max()}")
    
    # Test 4: Save screenshot
    try:
        cv2.imwrite("test_screenshot.png", screen)
        print("[OK] Screenshot saved as 'test_screenshot.png'")
    except Exception as e:
        print(f"[WARN]  Could not save screenshot: {e}")
    
    # Test 5: Show screenshot (small window)
    try:
        # Resize for display
        display = cv2.resize(screen, (640, 480))
        cv2.imshow("Test Screenshot (Press any key to close)", display)
        print("[OK] Screenshot displayed - Press any key in window to close")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"[WARN]  Could not display screenshot: {e}")
    
    print("\n[OK] TEST 2 PASSED: Screen capture works!")
    
except Exception as e:
    print(f"[FAIL] TEST 2 FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("=" * 60)

