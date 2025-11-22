"""
Window Finder - Automatically finds Blockade 3D Classic window
Works with both windowed and fullscreen mode (2025)
"""
import win32gui
import win32con
import win32api
import time


class WindowFinder:
    """Find and manage Blockade 3D Classic window"""
    
    def __init__(self):
        self.window_handle = None
        self.window_rect = None
        self.window_title = "Blockade 3D Classic"
        self.alternative_titles = [
            "Blockade 3D Classic",  # Exact match first
            "Blockade 3D",  # Close match
            "Blockade",  # Short name (Steam version)
        ]
        # Note: "Blockade" is now included because Steam version uses this title
        
    def find_window(self):
        """Find Blockade 3D Classic window by title"""
        def callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                title_lower = window_title.lower()
                
                # EXCLUDE GUI window and other non-game windows
                if "aimbot" in title_lower or "gui" in title_lower or "cursor" in title_lower:
                    return True  # Skip GUI windows
                
                # Match "Blockade 3D Classic" (exact) - but not if it contains "Aimbot"
                if "blockade 3d classic" in title_lower and "aimbot" not in title_lower:
                    windows.append((hwnd, window_title))
                # Match "Blockade 3D" (close) - but not if it contains "Aimbot"
                elif "blockade 3d" in title_lower and "aimbot" not in title_lower:
                    windows.append((hwnd, window_title))
                # Match "Blockade" (exact match only, exclude GUI)
                elif title_lower == "blockade":
                    windows.append((hwnd, window_title))
            return True
        
        windows = []
        win32gui.EnumWindows(callback, windows)
        
        if windows:
            # Prefer exact match
            for hwnd, title in windows:
                if "Blockade 3D Classic" in title:
                    self.window_handle = hwnd
                    self.window_title = title
                    return hwnd
            
            # Fallback to first match
            self.window_handle = windows[0][0]
            self.window_title = windows[0][1]
            return windows[0][0]
        
        return None
    
    def get_window_rect(self):
        """Get window rectangle (left, top, right, bottom)"""
        if not self.window_handle:
            if not self.find_window():
                return None
        
        try:
            rect = win32gui.GetWindowRect(self.window_handle)
            self.window_rect = rect
            return rect
        except:
            return None
    
    def get_window_size(self):
        """Get window size (width, height)"""
        rect = self.get_window_rect()
        if rect:
            left, top, right, bottom = rect
            return (right - left, bottom - top)
        return None
    
    def is_fullscreen(self):
        """Check if window is in fullscreen mode"""
        if not self.window_handle:
            return False
        
        try:
            # Check if window is maximized
            placement = win32gui.GetWindowPlacement(self.window_handle)
            if placement[1] == win32con.SW_SHOWMAXIMIZED:
                return True
            
            # Check if window covers entire screen
            rect = self.get_window_rect()
            if rect:
                screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
                screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
                left, top, right, bottom = rect
                
                # Allow small margin for taskbar
                if (left <= 0 and top <= 0 and 
                    right >= screen_width - 10 and 
                    bottom >= screen_height - 50):
                    return True
        except:
            pass
        
        return False
    
    def get_game_region(self):
        """
        Get game region for screen capture
        Returns: (left, top, width, height) or None
        """
        rect = self.get_window_rect()
        if not rect:
            return None
        
        left, top, right, bottom = rect
        width = right - left
        height = bottom - top
        
        # For fullscreen, use entire window
        if self.is_fullscreen():
            return (left, top, width, height)
        
        # For windowed mode, account for title bar
        # Title bar is usually ~30-40 pixels
        title_bar_height = 40
        return (left, top + title_bar_height, width, height - title_bar_height)
    
    def wait_for_window(self, timeout=30):
        """Wait for window to appear"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.find_window():
                return True
            time.sleep(0.5)
        return False


# Global instance
window_finder = WindowFinder()

