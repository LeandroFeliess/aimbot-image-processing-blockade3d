"""
Complete Diagnose - Test alles stap voor stap
"""
import sys
import time
import traceback

print("=" * 70)
print("COMPLETE DIAGNOSE - Test alles wat er mis kan zijn")
print("=" * 70)
print()

errors = []
warnings = []

# Test 1: Imports
print("[TEST 1] Testing imports...")
try:
    import cv2
    import numpy as np
    import pyautogui
    import keyboard
    print("  [OK] Basic imports work")
except Exception as e:
    errors.append(f"Basic imports failed: {e}")
    print(f"  [FAIL] {e}")

try:
    from grabscreen import grab_screen
    print("  [OK] grabscreen imported")
except Exception as e:
    errors.append(f"grabscreen import failed: {e}")
    print(f"  [FAIL] {e}")

try:
    from window_finder import window_finder
    print("  [OK] window_finder imported")
except Exception as e:
    errors.append(f"window_finder import failed: {e}")
    print(f"  [FAIL] {e}")

try:
    from aimbot_gui import AimbotGUI
    print("  [OK] aimbot_gui imported")
except Exception as e:
    errors.append(f"aimbot_gui import failed: {e}")
    print(f"  [FAIL] {e}")

try:
    from wallhacks import wallhacks
    print("  [OK] wallhacks imported")
except Exception as e:
    errors.append(f"wallhacks import failed: {e}")
    print(f"  [FAIL] {e}")

try:
    from soft_aim import soft_aimbot
    print("  [OK] soft_aim imported")
except Exception as e:
    errors.append(f"soft_aim import failed: {e}")
    print(f"  [FAIL] {e}")

try:
    import config
    print("  [OK] config imported")
except Exception as e:
    errors.append(f"config import failed: {e}")
    print(f"  [FAIL] {e}")

print()

# Test 2: Window Detection
print("[TEST 2] Testing window detection...")
try:
    if window_finder.wait_for_window(timeout=3):
        print(f"  [OK] Window found: '{window_finder.window_title}'")
        game_region = window_finder.get_game_region()
        if game_region:
            print(f"  [OK] Game region: {game_region}")
        else:
            warnings.append("Game region is None")
            print("  [WARN] Game region is None")
    else:
        errors.append("Window NOT found - is Blockade 3D Classic running?")
        print("  [FAIL] Window NOT found!")
        print("  [INFO] Make sure Blockade 3D Classic is running!")
except Exception as e:
    errors.append(f"Window detection failed: {e}")
    print(f"  [FAIL] {e}")
    traceback.print_exc()

print()

# Test 3: Screen Capture
print("[TEST 3] Testing screen capture...")
try:
    if window_finder.window_handle:
        game_region = window_finder.get_game_region()
        if game_region:
            left, top, width, height = game_region
            screen = grab_screen(region=(left, top, left + width, top + height), use_window_finder=True)
            if screen is not None and screen.size > 0:
                print(f"  [OK] Screen captured: {screen.shape}")
            else:
                errors.append("Screen capture returned None or empty")
                print("  [FAIL] Screen capture failed!")
        else:
            errors.append("Cannot test screen capture - no game region")
            print("  [FAIL] No game region")
    else:
        warnings.append("Cannot test screen capture - no window")
        print("  [WARN] No window - skipping screen capture test")
except Exception as e:
    errors.append(f"Screen capture test failed: {e}")
    print(f"  [FAIL] {e}")
    traceback.print_exc()

print()

# Test 4: GUI
print("[TEST 4] Testing GUI...")
try:
    gui = AimbotGUI()
    print("  [OK] GUI created")
    
    # Test if GUI has required attributes
    if hasattr(gui, 'aimbot_enabled'):
        print("  [OK] GUI has aimbot_enabled attribute")
    else:
        errors.append("GUI missing aimbot_enabled attribute")
        print("  [FAIL] GUI missing aimbot_enabled")
    
    if hasattr(gui, 'soft_aim_enabled'):
        print("  [OK] GUI has soft_aim_enabled attribute")
    else:
        errors.append("GUI missing soft_aim_enabled attribute")
        print("  [FAIL] GUI missing soft_aim_enabled")
    
    if hasattr(gui, 'wallhacks_enabled'):
        print("  [OK] GUI has wallhacks_enabled attribute")
    else:
        errors.append("GUI missing wallhacks_enabled attribute")
        print("  [FAIL] GUI missing wallhacks_enabled")
    
except Exception as e:
    errors.append(f"GUI test failed: {e}")
    print(f"  [FAIL] {e}")
    traceback.print_exc()

print()

# Test 5: Wallhacks
print("[TEST 5] Testing wallhacks...")
try:
    wallhacks.enable()
    if wallhacks.enabled:
        print("  [OK] Wallhacks enabled")
    else:
        errors.append("Wallhacks.enable() did not set enabled=True")
        print("  [FAIL] Wallhacks not enabled after enable() call")
    
    wallhacks.disable()
    if not wallhacks.enabled:
        print("  [OK] Wallhacks disabled")
    else:
        errors.append("Wallhacks.disable() did not set enabled=False")
        print("  [FAIL] Wallhacks still enabled after disable() call")
except Exception as e:
    errors.append(f"Wallhacks test failed: {e}")
    print(f"  [FAIL] {e}")
    traceback.print_exc()

print()

# Test 6: Soft Aim
print("[TEST 6] Testing soft aim...")
try:
    if hasattr(soft_aimbot, 'soft_aim_towards_target'):
        print("  [OK] soft_aim_towards_target function exists")
    else:
        errors.append("soft_aimbot missing soft_aim_towards_target function")
        print("  [FAIL] soft_aim_towards_target function not found")
    
    # Test if it can be called (with dummy values)
    try:
        result = soft_aimbot.soft_aim_towards_target(100, 100)
        print(f"  [OK] soft_aim_towards_target can be called (returned: {result})")
    except Exception as e:
        errors.append(f"soft_aim_towards_target call failed: {e}")
        print(f"  [FAIL] Cannot call soft_aim_towards_target: {e}")
except Exception as e:
    errors.append(f"Soft aim test failed: {e}")
    print(f"  [FAIL] {e}")
    traceback.print_exc()

print()

# Test 7: Config
print("[TEST 7] Testing config...")
try:
    required_configs = [
        'SCREEN_WIDTH', 'SCREEN_HEIGHT', 'THRESHOLD_VALUE',
        'INT_SUBDIV', 'SOFT_AIM_ENABLED', 'SOFT_AIM_STRENGTH'
    ]
    
    for cfg in required_configs:
        if hasattr(config, cfg):
            value = getattr(config, cfg)
            print(f"  [OK] config.{cfg} = {value}")
        else:
            errors.append(f"config missing {cfg}")
            print(f"  [FAIL] config.{cfg} not found")
except Exception as e:
    errors.append(f"Config test failed: {e}")
    print(f"  [FAIL] {e}")
    traceback.print_exc()

print()

# Test 8: Main script can be imported
print("[TEST 8] Testing main script import...")
try:
    # Try to import main functions
    import importlib.util
    spec = importlib.util.spec_from_file_location("main_module", "main_074_3.6.5.py")
    if spec and spec.loader:
        print("  [OK] Main script can be loaded")
    else:
        errors.append("Main script spec is None")
        print("  [FAIL] Main script spec is None")
except Exception as e:
    warnings.append(f"Main script import test: {e}")
    print(f"  [WARN] {e}")

print()

# Summary
print("=" * 70)
print("DIAGNOSE SUMMARY")
print("=" * 70)
print()

if errors:
    print(f"[FAIL] {len(errors)} ERRORS found:")
    for i, error in enumerate(errors, 1):
        print(f"  {i}. {error}")
    print()
else:
    print("[OK] No errors found!")
    print()

if warnings:
    print(f"[WARN] {len(warnings)} WARNINGS:")
    for i, warning in enumerate(warnings, 1):
        print(f"  {i}. {warning}")
    print()

if not errors:
    print("[OK] All basic tests passed!")
    print("[INFO] If aimbot still doesn't work, the problem is in the main loop")
    print("[INFO] Check if:")
    print("  1. Main loop is running (check terminal output)")
    print("  2. Targets are being detected (check for 'Target detected!' messages)")
    print("  3. GUI toggles are working (check GUI buttons)")
    print("  4. TAB key is NOT pressed (TAB pauses aimbot)")
else:
    print("[FAIL] Fix the errors above first!")
    print()

print("=" * 70)

