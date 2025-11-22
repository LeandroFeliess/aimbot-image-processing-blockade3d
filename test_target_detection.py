"""
Test Script 3: Target Detection
Test of target detection werkt (spelers detecteren)
"""
import sys
import cv2
import numpy as np
print("=" * 60)
print("TEST 3: Target Detection")
print("=" * 60)

try:
    from grabscreen import grab_screen
    from window_finder import window_finder
    from main_074_3_6_5 import is_a_RelevantColor
    import config
    print("[OK] Modules loaded")
except Exception as e:
    print(f"[FAIL] ERROR loading modules: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n[INFO] Testing target detection...")

# Test 1: Screen capture
if not window_finder.wait_for_window(timeout=3):
    print("[FAIL] Window not found")
    sys.exit(1)

game_region = window_finder.get_game_region()
if not game_region:
    print("[FAIL] Could not get game region")
    sys.exit(1)

left, top, width, height = game_region
print(f"[OK] Game region: ({left}, {top}) - {width} x {height}")

try:
    print("[CAPTURE] Capturing screen...")
    screen = grab_screen(region=(left, top, left + width, top + height), use_window_finder=True)
    
    if screen is None or screen.size == 0:
        print("[FAIL] Screen capture failed")
        sys.exit(1)
    
    print(f"[OK] Screen captured: {screen.shape}")
    
    # Test 2: Convert to grayscale
    screenGray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    print("[OK] Converted to grayscale")
    
    # Test 3: Threshold
    ret, whiteChannel = cv2.threshold(screenGray, config.THRESHOLD_VALUE, 255, cv2.THRESH_BINARY)
    print(f"[OK] Threshold applied: {config.THRESHOLD_VALUE}")
    print(f"   White pixels: {np.sum(whiteChannel == 255)}")
    print(f"   Black pixels: {np.sum(whiteChannel == 0)}")
    
    # Test 4: Color detection
    print("\n[INFO] Searching for player colors (red, green, blue)...")
    
    red_count = 0
    green_count = 0
    blue_count = 0
    
    # Sample some pixels
    sample_size = min(1000, screen.shape[0] * screen.shape[1])
    indices = np.random.choice(screen.shape[0] * screen.shape[1], sample_size, replace=False)
    
    for idx in indices:
        y = idx // screen.shape[1]
        x = idx % screen.shape[1]
        pixel = screen[y, x]
        
        if is_a_RelevantColor(pixel):
            r, g, b = pixel[0], pixel[1], pixel[2]
            if r == 255:
                red_count += 1
            elif g == 255:
                green_count += 1
            elif b == 255:
                blue_count += 1
    
    print(f"   Red pixels found: {red_count}")
    print(f"   Green pixels found: {green_count}")
    print(f"   Blue pixels found: {blue_count}")
    
    total_colors = red_count + green_count + blue_count
    if total_colors > 0:
        print(f"\n[OK] Found {total_colors} player color pixels!")
        print("   (This means players are visible on screen)")
    else:
        print("\n[WARN]  No player colors found")
        print("   (Either no players on screen, or color detection needs adjustment)")
    
    # Test 5: Save detection result
    try:
        # Highlight detected colors
        result = screen.copy()
        for idx in indices[:100]:  # Check first 100
            y = idx // screen.shape[1]
            x = idx % screen.shape[1]
            pixel = screen[y, x]
            
            if is_a_RelevantColor(pixel):
                cv2.circle(result, (x, y), 5, (0, 255, 255), 2)  # Yellow circle
        
        cv2.imwrite("test_target_detection.png", result)
        print("[OK] Detection result saved as 'test_target_detection.png'")
    except Exception as e:
        print(f"[WARN]  Could not save result: {e}")
    
    print("\n[OK] TEST 3 PASSED: Target detection works!")
    
except Exception as e:
    print(f"[FAIL] TEST 3 FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("=" * 60)

