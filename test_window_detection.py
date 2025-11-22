"""
Test Script 1: Window Detection
Test of Blockade 3D Classic window wordt gevonden
"""
import sys
print("=" * 60)
print("TEST 1: Window Detection")
print("=" * 60)

try:
    from window_finder import window_finder
    print("[OK] window_finder module loaded")
except Exception as e:
    print(f"[ERROR] ERROR loading window_finder: {e}")
    sys.exit(1)

print("\n[INFO] Searching for Blockade 3D Classic window...")
if window_finder.wait_for_window(timeout=5):
    print(f"[OK] Window found: '{window_finder.window_title}'")
    print(f"   Window Handle: {window_finder.window_handle}")
    
    rect = window_finder.get_window_rect()
    if rect:
        left, top, right, bottom = rect
        print(f"   Position: ({left}, {top})")
        print(f"   Size: {right - left} x {bottom - top}")
    
    size = window_finder.get_window_size()
    if size:
        print(f"   Window Size: {size[0]} x {size[1]}")
    
    is_fullscreen = window_finder.is_fullscreen()
    print(f"   Fullscreen: {is_fullscreen}")
    
    game_region = window_finder.get_game_region()
    if game_region:
        left, top, width, height = game_region
        print(f"   Game Region: ({left}, {top}) - {width} x {height}")
    
    print("\n[OK] TEST 1 PASSED: Window detection works!")
else:
    print("[FAIL] TEST 1 FAILED: Window NOT found!")
    print("   Make sure Blockade 3D Classic is running!")
    print("\n   Searching for all visible windows...")
    
    # List all windows
    try:
        import win32gui
        def callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title:
                    windows.append((hwnd, title))
            return True
        
        all_windows = []
        win32gui.EnumWindows(callback, all_windows)
        
        print(f"   Found {len(all_windows)} visible windows:")
        for hwnd, title in all_windows[:20]:  # Show first 20
            print(f"     - '{title}'")
    except Exception as e:
        print(f"   Could not list windows: {e}")

print("=" * 60)

