"""
Test Main Loop - Simuleer de main loop om te zien wat er gebeurt
"""
import sys
import time
import cv2
import numpy as np

print("=" * 70)
print("MAIN LOOP TEST - Simuleer wat de aimbot doet")
print("=" * 70)
print()

try:
    from grabscreen import grab_screen
    from window_finder import window_finder
    import config
    
    # Define is_a_RelevantColor
    def is_a_RelevantColor(tmpScreenRGBpixel):
        r, g, b = tmpScreenRGBpixel[0], tmpScreenRGBpixel[1], tmpScreenRGBpixel[2]
        try:
            muzzle_threshold = config.MUZZLE_FLASH_THRESHOLD
        except:
            muzzle_threshold = 200
        
        if r > muzzle_threshold and g > muzzle_threshold and b > muzzle_threshold:
            return False
        
        if (r == 255) and (g < config.COLOR_THRESHOLD) and (b < config.COLOR_THRESHOLD):
            return True
        if (r < config.COLOR_THRESHOLD) and (g == 255) and (b < config.COLOR_THRESHOLD):
            return True
        if (r < config.COLOR_THRESHOLD) and (g < config.COLOR_THRESHOLD) and (b == 255):
            return True
        return False
    
    print("[OK] Modules loaded")
except Exception as e:
    print(f"[FAIL] Import failed: {e}")
    sys.exit(1)

# Test window
if not window_finder.wait_for_window(timeout=3):
    print("[FAIL] Window not found!")
    sys.exit(1)

print(f"[OK] Window found: '{window_finder.window_title}'")
game_region = window_finder.get_game_region()
if not game_region:
    print("[FAIL] No game region!")
    sys.exit(1)

left, top, width, height = game_region
print(f"[OK] Game region: ({left}, {top}) - {width} x {height}")
print()

# Simulate main loop for 5 iterations
print("[INFO] Simulating main loop (5 iterations)...")
print()

for iteration in range(5):
    print(f"[ITERATION {iteration + 1}]")
    
    # Capture screen
    try:
        screen = grab_screen(region=(left, top, left + width, top + height), use_window_finder=True)
        if screen is None or screen.size == 0:
            print("  [FAIL] Screen capture failed")
            continue
        print(f"  [OK] Screen captured: {screen.shape}")
    except Exception as e:
        print(f"  [FAIL] Screen capture error: {e}")
        continue
    
    # Process
    try:
        screenGray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        ret, whiteChannel = cv2.threshold(screenGray, config.THRESHOLD_VALUE, 255, cv2.THRESH_BINARY)
        print(f"  [OK] Threshold applied: {np.sum(whiteChannel == 255)} white pixels")
    except Exception as e:
        print(f"  [FAIL] Processing error: {e}")
        continue
    
    # Search for targets
    try:
        intSubdiv = config.INT_SUBDIV
        iix = 168
        iiy = 0
        targets_found = 0
        
        # Limited search
        for _ in range(min(50, screen.shape[0] // intSubdiv)):
            for _ in range(min(50, screen.shape[1] // intSubdiv)):
                if iix < screen.shape[0] and iiy < screen.shape[1]:
                    if whiteChannel[iix, iiy] == 255:
                        # Check for color
                        if 0 <= iix < screen.shape[0] and 0 <= iiy < screen.shape[1]:
                            pixel = screen[iix, iiy]
                            if is_a_RelevantColor(pixel):
                                targets_found += 1
                                if targets_found == 1:  # Print first target
                                    print(f"  [OK] Target found at ({iix}, {iiy})")
                iiy += intSubdiv
            iiy = 0
            iix += intSubdiv
        
        if targets_found > 0:
            print(f"  [OK] Total targets found: {targets_found}")
        else:
            print("  [WARN] No targets found")
    except Exception as e:
        print(f"  [FAIL] Target search error: {e}")
        traceback.print_exc()
    
    print()
    time.sleep(0.5)  # Small delay

print("=" * 70)
print("MAIN LOOP TEST COMPLETE")
print("=" * 70)
print()
print("If targets were found, detection works!")
print("If no targets were found, check:")
print("  1. Are there players on screen?")
print("  2. Is THRESHOLD_VALUE correct?")
print("  3. Is COLOR_THRESHOLD correct?")

