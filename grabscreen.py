# Done by Frannecklp
# Updated 2025 for fullscreen support and anti-cheat bypass

import cv2
import numpy as np
import win32gui, win32ui, win32con, win32api
from window_finder import window_finder

def grab_screen(region=None, use_window_finder=True):
    """
    Grab screen - supports both windowed and fullscreen mode (2025)
    
    Args:
        region: (left, top, width, height) or None for auto-detect
        use_window_finder: Use automatic window detection
    """
    
    # Try to find game window automatically
    if use_window_finder and region is None:
        game_region = window_finder.get_game_region()
        if game_region:
            left, top, width, height = game_region
            region = (left, top, left + width, top + height)
    
    if region:
        left, top, x2, y2 = region
        width = x2 - left + 1
        height = y2 - top + 1
        hwin = win32gui.GetDesktopWindow()
    else:
        # Fallback to desktop window
        hwin = win32gui.GetDesktopWindow()
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
    
    signedIntsArray = bmp.GetBitmapBits(True)
    # Fix: np.fromstring is deprecated, use np.frombuffer instead
    img = np.frombuffer(signedIntsArray, dtype='uint8')
    # img.shape = (height,width,4)
    img.shape = (height,width,4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
