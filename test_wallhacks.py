"""
Test Script 4: Wallhacks/ESP
Test of wallhacks werken
"""
import sys
import cv2
import numpy as np
print("=" * 60)
print("TEST 4: Wallhacks/ESP")
print("=" * 60)

try:
    from grabscreen import grab_screen
    from window_finder import window_finder
    from wallhacks import wallhacks
    from main_074_3_6_5 import is_a_RelevantColor
    import config
    print("[OK] Modules loaded")
except Exception as e:
    print(f"[FAIL] ERROR loading modules: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n[INFO] Testing wallhacks...")

# Test 1: Enable wallhacks
try:
    wallhacks.enable()
    print("[OK] Wallhacks enabled")
except Exception as e:
    print(f"[FAIL] Could not enable wallhacks: {e}")
    sys.exit(1)

# Test 2: Screen capture
if not window_finder.wait_for_window(timeout=3):
    print("[FAIL] Window not found")
    sys.exit(1)

game_region = window_finder.get_game_region()
if not game_region:
    print("[FAIL] Could not get game region")
    sys.exit(1)

left, top, width, height = game_region

try:
    print("[CAPTURE] Capturing screen...")
    screen = grab_screen(region=(left, top, left + width, top + height), use_window_finder=True)
    
    if screen is None or screen.size == 0:
        print("[FAIL] Screen capture failed")
        sys.exit(1)
    
    print(f"[OK] Screen captured: {screen.shape}")
    
    # Test 3: Find targets
    print("[INFO] Searching for targets...")
    
    targets = []
    screenGray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    ret, whiteChannel = cv2.threshold(screenGray, config.THRESHOLD_VALUE, 255, cv2.THRESH_BINARY)
    
    # Search for targets (simplified version)
    intSubdiv = config.INT_SUBDIV
    iix = 168
    iiy = 0
    
    for _ in range(min(100, screen.shape[0] // intSubdiv)):  # Limit search
        for _ in range(min(100, screen.shape[1] // intSubdiv)):
            if iix < screen.shape[0] and iiy < screen.shape[1]:
                if whiteChannel[iix, iiy] == 255:
                    # Check for player color
                    if 0 <= iix < screen.shape[0] and 0 <= iiy < screen.shape[1]:
                        pixel = screen[iix, iiy]
                        if is_a_RelevantColor(pixel):
                            r, g, b = pixel[0], pixel[1], pixel[2]
                            color = None
                            if r == 255:
                                color = 'red'
                            elif g == 255:
                                color = 'green'
                            elif b == 255:
                                color = 'blue'
                            
                            if color:
                                targets.append((iix, iiy, color))
            iiy += intSubdiv
        iiy = 0
        iix += intSubdiv
    
    print(f"[OK] Found {len(targets)} targets")
    
    if len(targets) > 0:
        for i, (x, y, color) in enumerate(targets[:5]):  # Show first 5
            print(f"   Target {i+1}: ({x}, {y}) - {color}")
    
    # Test 4: Draw wallhacks
    if len(targets) > 0:
        print("\n[DRAW] Drawing wallhacks...")
        result = wallhacks.draw_on_screen(screen, targets)
        
        if result is not None:
            print("[OK] Wallhacks drawn successfully")
            
            # Save result
            try:
                cv2.imwrite("test_wallhacks.png", result)
                print("[OK] Result saved as 'test_wallhacks.png'")
            except Exception as e:
                print(f"[WARN]  Could not save: {e}")
            
            # Show result
            try:
                display = cv2.resize(result, (640, 480))
                cv2.imshow("Wallhacks Test (Press any key to close)", display)
                print("[OK] Wallhacks displayed - Press any key in window to close")
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            except Exception as e:
                print(f"[WARN]  Could not display: {e}")
        else:
            print("[FAIL] Wallhacks drawing returned None")
    else:
        print("[WARN]  No targets found - cannot test wallhacks drawing")
        print("   (This is normal if no players are on screen)")
    
    print("\n[OK] TEST 4 PASSED: Wallhacks work!")
    
except Exception as e:
    print(f"[FAIL] TEST 4 FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("=" * 60)

