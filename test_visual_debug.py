"""
Visual Debug Test - Maakt screenshots en toont wat de aimbot ziet
"""
import sys
import cv2
import numpy as np
import time
print("=" * 60)
print("VISUAL DEBUG TEST")
print("=" * 60)
print()
print("Dit script maakt screenshots en toont:")
print("1. Wat de aimbot ziet (screen capture)")
print("2. Waar targets worden gedetecteerd")
print("3. Wallhacks/ESP overlay")
print()
print("Druk op een toets in de OpenCV windows om door te gaan")
print("=" * 60)
print()

try:
    from grabscreen import grab_screen
    from window_finder import window_finder
    from wallhacks import wallhacks
    import config
    
    # Define is_a_RelevantColor function directly (from main_074_3.6.5.py)
    def is_a_RelevantColor(tmpScreenRGBpixel):
        """Check if pixel is a player color (red, green, or blue)"""
        r, g, b = tmpScreenRGBpixel[0], tmpScreenRGBpixel[1], tmpScreenRGBpixel[2]
        
        # Filter out muzzle flash
        try:
            muzzle_threshold = config.MUZZLE_FLASH_THRESHOLD
        except:
            muzzle_threshold = 200
        
        if r > muzzle_threshold and g > muzzle_threshold and b > muzzle_threshold:
            return False  # Likely muzzle flash
        
        # Check for pure red player
        if (r == 255) and (g < config.COLOR_THRESHOLD) and (b < config.COLOR_THRESHOLD):
            return True
        
        # Check for pure green player
        if (r < config.COLOR_THRESHOLD) and (g == 255) and (b < config.COLOR_THRESHOLD):
            return True
        
        # Check for pure blue player
        if (r < config.COLOR_THRESHOLD) and (g < config.COLOR_THRESHOLD) and (b == 255):
            return True
        
        return False
    
    print("[OK] Modules loaded")
except Exception as e:
    print(f"[FAIL] ERROR loading modules: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 1: Window detection
print("[INFO] Step 1: Window Detection...")
if not window_finder.wait_for_window(timeout=5):
    print("[FAIL] Window NOT found!")
    print("   Zorg dat Blockade 3D Classic DRAAT!")
    sys.exit(1)

print(f"[OK] Window found: '{window_finder.window_title}'")
game_region = window_finder.get_game_region()
if not game_region:
    print("[FAIL] Could not get game region")
    sys.exit(1)

left, top, width, height = game_region
print(f"[OK] Game region: ({left}, {top}) - {width} x {height}")
print()

# Test 2: Screen capture
print("[INFO] Step 2: Screen Capture...")
screen = grab_screen(region=(left, top, left + width, top + height), use_window_finder=True)

if screen is None or screen.size == 0:
    print("[FAIL] Screen capture failed!")
    sys.exit(1)

print(f"[OK] Screen captured: {screen.shape}")
cv2.imwrite("debug_1_original_screen.png", screen)
print("[OK] Screenshot saved: debug_1_original_screen.png")
print()

# Test 3: Grayscale + Threshold
print("[INFO] Step 3: Processing (Grayscale + Threshold)...")
screenGray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
ret, whiteChannel = cv2.threshold(screenGray, config.THRESHOLD_VALUE, 255, cv2.THRESH_BINARY)

# Show threshold result
cv2.imwrite("debug_2_threshold.png", whiteChannel)
print("[OK] Threshold saved: debug_2_threshold.png")
print()

# Test 4: Target Detection
print("[INFO] Step 4: Target Detection...")
targets = []
target_image = screen.copy()

# Search for targets
intSubdiv = config.INT_SUBDIV
iix = 168
iiy = 0
target_count = 0

print(f"   Searching with INT_SUBDIV={intSubdiv}...")
print(f"   Starting at position: ({iix}, {iiy})")

for line_num in range(min(200, screen.shape[0] // intSubdiv)):
    for col_num in range(min(200, screen.shape[1] // intSubdiv)):
        if iix < screen.shape[0] and iiy < screen.shape[1]:
            # Check for white outline
            if whiteChannel[iix, iiy] == 255:
                # Check surrounding pixels for player color
                found_color = False
                color_name = None
                
                for check_x in range(max(0, iix-2), min(screen.shape[0], iix+3)):
                    for check_y in range(max(0, iiy-2), min(screen.shape[1], iiy+3)):
                        pixel = screen[check_x, check_y]
                        if is_a_RelevantColor(pixel):
                            r, g, b = pixel[0], pixel[1], pixel[2]
                            if r == 255:
                                color_name = 'red'
                            elif g == 255:
                                color_name = 'green'
                            elif b == 255:
                                color_name = 'blue'
                            
                            if color_name:
                                found_color = True
                                targets.append((iix, iiy, color_name))
                                
                                # Draw on target image
                                if color_name == 'red':
                                    cv2.circle(target_image, (iiy, iix), 10, (0, 0, 255), 2)
                                elif color_name == 'green':
                                    cv2.circle(target_image, (iiy, iix), 10, (0, 255, 0), 2)
                                elif color_name == 'blue':
                                    cv2.circle(target_image, (iiy, iix), 10, (255, 0, 0), 2)
                                
                                target_count += 1
                                break
                    
                    if found_color:
                        break
        iiy += intSubdiv
    iiy = 0
    iix += intSubdiv

print(f"[OK] Found {len(targets)} targets")
if len(targets) > 0:
    for i, (x, y, color) in enumerate(targets[:10]):
        print(f"   Target {i+1}: ({x}, {y}) - {color}")
else:
    print("[WARN] No targets found!")
    print("   Mogelijke oorzaken:")
    print("   - Geen spelers op scherm")
    print("   - THRESHOLD_VALUE te hoog/laag")
    print("   - COLOR_THRESHOLD te hoog/laag")
    print("   - Verkeerde ROI (Region of Interest)")

cv2.imwrite("debug_3_targets_detected.png", target_image)
print("[OK] Target detection saved: debug_3_targets_detected.png")
print()

# Test 5: Wallhacks
print("[INFO] Step 5: Wallhacks/ESP...")
if len(targets) > 0:
    wallhacks.enable()
    wallhacks_image = wallhacks.draw_on_screen(screen, targets)
    cv2.imwrite("debug_4_wallhacks.png", wallhacks_image)
    print("[OK] Wallhacks saved: debug_4_wallhacks.png")
else:
    print("[WARN] No targets - skipping wallhacks")
print()

# Show all images
print("[INFO] Displaying images (druk op toets om door te gaan)...")
print()

# Resize for display
def show_image(title, image, wait=True):
    display = cv2.resize(image, (960, 540))
    cv2.imshow(title, display)
    if wait:
        print(f"   {title} - Druk op toets om door te gaan...")
        cv2.waitKey(0)
    else:
        cv2.waitKey(1)

try:
    show_image("1. Original Screen (Origineel scherm)", screen)
    show_image("2. Threshold (Witte outlines)", whiteChannel)
    show_image("3. Targets Detected (Gedetecteerde targets)", target_image)
    
    if len(targets) > 0:
        wallhacks_image = wallhacks.draw_on_screen(screen, targets)
        show_image("4. Wallhacks/ESP (ESP overlay)", wallhacks_image)
    
    cv2.destroyAllWindows()
except Exception as e:
    print(f"[WARN] Could not display images: {e}")

print()
print("=" * 60)
print("TEST COMPLETE!")
print("=" * 60)
print()
print("Screenshots opgeslagen:")
print("  - debug_1_original_screen.png (Origineel scherm)")
print("  - debug_2_threshold.png (Threshold/witte outlines)")
print("  - debug_3_targets_detected.png (Gedetecteerde targets)")
if len(targets) > 0:
    print("  - debug_4_wallhacks.png (Wallhacks/ESP)")
print()
print("Analyseer deze screenshots om te zien wat er werkt/niet werkt!")
print("=" * 60)

