"""
Test Actual Functionality - Test of soft aim en wallhacks ECHT werken
"""
import sys
import time
import cv2
import numpy as np
import pyautogui

print("=" * 70)
print("ACTUAL FUNCTIONALITY TEST")
print("=" * 70)
print()
print("Dit test of soft aim en wallhacks ECHT werken")
print("=" * 70)
print()

try:
    from grabscreen import grab_screen
    from window_finder import window_finder
    from wallhacks import wallhacks
    from soft_aim import soft_aimbot
    import config
    
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

# Setup
if not window_finder.wait_for_window(timeout=3):
    print("[FAIL] Window not found!")
    sys.exit(1)

game_region = window_finder.get_game_region()
if not game_region:
    print("[FAIL] No game region!")
    sys.exit(1)

left, top, width, height = game_region
print(f"[OK] Game region: ({left}, {top}) - {width} x {height}")
print()

# TEST 1: Soft Aim - Test of muis echt beweegt
print("[TEST 1] Testing Soft Aim - Does mouse actually move?")
print("  Moving mouse to center of screen first...")
screen_center_x = left + width // 2
screen_center_y = top + height // 2
pyautogui.moveTo(screen_center_x, screen_center_y, duration=0.5)
time.sleep(0.5)

current_pos = pyautogui.position()
print(f"  Current mouse position: {current_pos}")

# Enable soft aim
config.SOFT_AIM_ENABLED = True
print("  Soft aim enabled in config")

# Test soft aim towards a target
test_target_x = current_pos[0] + 100
test_target_y = current_pos[1] + 50
print(f"  Testing soft aim towards: ({test_target_x}, {test_target_y})")

result = soft_aimbot.soft_aim_towards_target(test_target_x, test_target_y)
print(f"  soft_aim_towards_target returned: {result}")

time.sleep(1)  # Wait for movement
new_pos = pyautogui.position()
print(f"  New mouse position: {new_pos}")

if new_pos != current_pos:
    print("  [OK] Mouse moved! Soft aim works!")
    distance = ((new_pos[0] - current_pos[0])**2 + (new_pos[1] - current_pos[1])**2)**0.5
    print(f"  Distance moved: {distance:.1f} pixels")
else:
    print("  [FAIL] Mouse did NOT move! Soft aim does NOT work!")
    print("  Possible reasons:")
    print("    - Target too far away (max distance check)")
    print("    - Cooldown active")
    print("    - Soft aim function returns False")

print()

# TEST 2: Wallhacks - Test of ESP echt zichtbaar is
print("[TEST 2] Testing Wallhacks - Is ESP window visible?")
wallhacks.enable()
print(f"  wallhacks.enabled: {wallhacks.enabled}")

# Capture screen
screen = grab_screen(region=(left, top, left + width, top + height), use_window_finder=True)
if screen is None:
    print("  [FAIL] Cannot test - screen capture failed")
else:
    print(f"  Screen captured: {screen.shape}")
    
    # Create fake targets
    fake_targets = [
        (screen.shape[0] // 2, screen.shape[1] // 2, 'red'),
        (screen.shape[0] // 3, screen.shape[1] // 3, 'green'),
        (screen.shape[0] // 4, screen.shape[1] // 4, 'blue'),
    ]
    print(f"  Created {len(fake_targets)} fake targets for testing")
    
    # Draw wallhacks
    result = wallhacks.draw_on_screen(screen, fake_targets)
    print(f"  wallhacks.draw_on_screen returned: {type(result)}")
    
    # Check if OpenCV window exists
    try:
        # Try to get window property
        cv2.namedWindow('Wallhacks ESP', cv2.WINDOW_NORMAL)
        print("  [OK] OpenCV window 'Wallhacks ESP' can be created")
        print("  [INFO] Check if you see a window with ESP boxes!")
        print("  [INFO] If no window appears, wallhacks are not visible")
        
        # Show for 3 seconds
        cv2.imshow('Wallhacks ESP', cv2.resize(result, (640, 360)))
        print("  [INFO] Window shown - press any key in window to continue...")
        cv2.waitKey(3000)  # Wait 3 seconds
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"  [FAIL] Cannot show window: {e}")

print()

# TEST 3: Check main loop integration
print("[TEST 3] Testing Main Loop Integration")
print("  Checking if main loop would call these functions...")

# Simulate what main loop does
screen = grab_screen(region=(left, top, left + width, top + height), use_window_finder=True)
if screen is not None:
    screenGray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    ret, whiteChannel = cv2.threshold(screenGray, config.THRESHOLD_VALUE, 255, cv2.THRESH_BINARY)
    
    # Search for real targets
    intSubdiv = config.INT_SUBDIV
    iix = 168
    iiy = 0
    wallhacks_targets = []
    target_found = False
    Xoffset = 0
    Yoffset = 0
    
    print("  Searching for targets...")
    for _ in range(min(50, screen.shape[0] // intSubdiv)):
        for _ in range(min(50, screen.shape[1] // intSubdiv)):
            if iix < screen.shape[0] and iiy < screen.shape[1]:
                if whiteChannel[iix, iiy] == 255:
                    if 0 <= iix < screen.shape[0] and 0 <= iiy < screen.shape[1]:
                        pixel = screen[iix, iiy]
                        if is_a_RelevantColor(pixel):
                            r, g, b = pixel[0], pixel[1], pixel[2]
                            color = 'red' if r == 255 else ('green' if g == 255 else 'blue')
                            wallhacks_targets.append((iix, iiy, color))
                            
                            if not target_found:
                                target_found = True
                                current_x, current_y = pyautogui.position()
                                Xoffset = iiy - current_x
                                Yoffset = iix - current_y
                                print(f"  [OK] Target found at ({iix}, {iiy}) - {color}")
                                print(f"      Xoffset: {Xoffset}, Yoffset: {Yoffset}")
            iiy += intSubdiv
        iiy = 0
        iix += intSubdiv
    
    if target_found:
        print(f"  [OK] Found {len(wallhacks_targets)} targets")
        
        # Test wallhacks
        if wallhacks.enabled:
            print("  Testing wallhacks with real targets...")
            result = wallhacks.draw_on_screen(screen, wallhacks_targets)
            print(f"  [OK] Wallhacks drawn")
        
        # Test soft aim
        if config.SOFT_AIM_ENABLED:
            print("  Testing soft aim with real target...")
            current_x, current_y = pyautogui.position()
            target_x = current_x + Xoffset
            target_y = current_y + Yoffset
            try:
                head_offset = config.SOFT_AIM_HEAD_OFFSET
            except:
                head_offset = -15
            target_y += head_offset
            
            print(f"  Current mouse: ({current_x}, {current_y})")
            print(f"  Target: ({target_x}, {target_y})")
            
            result = soft_aimbot.soft_aim_towards_target(target_x, target_y)
            print(f"  soft_aim_towards_target returned: {result}")
            
            time.sleep(0.5)
            new_pos = pyautogui.position()
            if new_pos != (current_x, current_y):
                print(f"  [OK] Mouse moved from ({current_x}, {current_y}) to {new_pos}")
            else:
                print(f"  [FAIL] Mouse did NOT move!")
    else:
        print("  [WARN] No targets found - cannot test with real targets")
        print("         Make sure there are players on screen!")

print()
print("=" * 70)
print("TEST COMPLETE")
print("=" * 70)
print()
print("SUMMARY:")
print("  - If soft aim mouse moved: Soft aim WORKS")
print("  - If wallhacks window appeared: Wallhacks WORKS")
print("  - If neither worked: Check the errors above")
print()

