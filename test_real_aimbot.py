"""
Test Real Aimbot - Simuleer de echte main loop met GUI checks
"""
import sys
import time
import keyboard

print("=" * 70)
print("REAL AIMBOT TEST - Simuleer wat er echt gebeurt")
print("=" * 70)
print()
print("Dit test de echte main loop logica")
print("Druk op CTRL+C om te stoppen")
print("=" * 70)
print()

try:
    from grabscreen import grab_screen
    from window_finder import window_finder
    from aimbot_gui import AimbotGUI
    from wallhacks import wallhacks
    from soft_aim import soft_aimbot
    import config
    import cv2
    import numpy as np
    import pyautogui
    
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
    
    print("[OK] All modules loaded")
except Exception as e:
    print(f"[FAIL] Import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Setup
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

# Create GUI (but don't show it)
gui = AimbotGUI()
print("[OK] GUI created")
print(f"  - aimbot_enabled: {gui.aimbot_enabled}")
print(f"  - soft_aim_enabled: {gui.soft_aim_enabled}")
print(f"  - wallhacks_enabled: {gui.wallhacks_enabled}")
print()

# Enable features for testing
print("[INFO] Enabling features for test...")
gui.soft_aim_enabled = True
gui.wallhacks_enabled = True
wallhacks.enable()
print(f"  - soft_aim_enabled: {gui.soft_aim_enabled}")
print(f"  - wallhacks_enabled: {gui.wallhacks_enabled}")
print(f"  - wallhacks.enabled: {wallhacks.enabled}")
print()

# Main loop simulation
print("[INFO] Starting main loop simulation...")
print("[INFO] Press CTRL+C to stop")
print()

iteration = 0
targets_detected = 0
soft_aim_activations = 0
wallhacks_draws = 0

try:
    while True:
        iteration += 1
        
        # Capture screen
        screen = grab_screen(region=(left, top, left + width, top + height), use_window_finder=True)
        if screen is None or screen.size == 0:
            continue
        
        # Process
        screenGray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        ret, whiteChannel = cv2.threshold(screenGray, config.THRESHOLD_VALUE, 255, cv2.THRESH_BINARY)
        
        # Search for targets
        intSubdiv = config.INT_SUBDIV
        iix = 168
        iiy = 0
        wallhacks_targets = []
        target_found = False
        Xoffset = 0
        Yoffset = 0
        
        for _ in range(min(100, screen.shape[0] // intSubdiv)):
            for _ in range(min(100, screen.shape[1] // intSubdiv)):
                if iix < screen.shape[0] and iiy < screen.shape[1]:
                    if whiteChannel[iix, iiy] == 255:
                        # Check for color
                        if 0 <= iix < screen.shape[0] and 0 <= iiy < screen.shape[1]:
                            pixel = screen[iix, iiy]
                            if is_a_RelevantColor(pixel):
                                r, g, b = pixel[0], pixel[1], pixel[2]
                                color = 'red' if r == 255 else ('green' if g == 255 else 'blue')
                                wallhacks_targets.append((iix, iiy, color))
                                
                                if not target_found:
                                    target_found = True
                                    targets_detected += 1
                                    Xoffset = iiy - pyautogui.position()[0]
                                    Yoffset = iix - pyautogui.position()[1]
                                    print(f"[ITERATION {iteration}] Target detected! ({iix}, {iiy}) - {color}")
                iiy += intSubdiv
            iiy = 0
            iix += intSubdiv
        
        # Wallhacks
        if wallhacks.enabled and len(wallhacks_targets) > 0:
            wallhacks.draw_on_screen(screen, wallhacks_targets)
            wallhacks_draws += 1
            if wallhacks_draws % 10 == 1:  # Print every 10th time
                print(f"  [WALLHACKS] Drawing ESP for {len(wallhacks_targets)} targets")
        
        # Soft Aim
        if target_found and gui.soft_aim_enabled and not gui.aimbot_enabled:
            if not keyboard.is_pressed('tab'):
                current_x, current_y = pyautogui.position()
                target_x = current_x + Xoffset
                target_y = current_y + Yoffset
                
                try:
                    head_offset = config.SOFT_AIM_HEAD_OFFSET
                except:
                    head_offset = -15
                target_y += head_offset
                
                if soft_aimbot.soft_aim_towards_target(target_x, target_y):
                    soft_aim_activations += 1
                    if soft_aim_activations % 5 == 1:  # Print every 5th time
                        print(f"  [SOFT AIM] Activated! Moving towards ({target_x}, {target_y})")
        
        # Status every 50 iterations
        if iteration % 50 == 0:
            print(f"[STATUS] Iterations: {iteration}, Targets: {targets_detected}, Soft Aim: {soft_aim_activations}, Wallhacks: {wallhacks_draws}")
        
        time.sleep(0.033)  # ~30 FPS
        
except KeyboardInterrupt:
    print()
    print("=" * 70)
    print("TEST STOPPED")
    print("=" * 70)
    print(f"Total iterations: {iteration}")
    print(f"Targets detected: {targets_detected}")
    print(f"Soft aim activations: {soft_aim_activations}")
    print(f"Wallhacks draws: {wallhacks_draws}")
    print()
    
    if targets_detected == 0:
        print("[PROBLEEM] Geen targets gedetecteerd!")
        print("  - Zijn er spelers op scherm?")
        print("  - Is THRESHOLD_VALUE correct?")
    elif soft_aim_activations == 0 and gui.soft_aim_enabled:
        print("[PROBLEEM] Soft aim wordt niet geactiveerd!")
        print("  - Check soft_aim_towards_target functie")
    elif wallhacks_draws == 0 and wallhacks.enabled:
        print("[PROBLEEM] Wallhacks worden niet getekend!")
        print("  - Check wallhacks.draw_on_screen functie")
    else:
        print("[OK] Alles werkt!")

