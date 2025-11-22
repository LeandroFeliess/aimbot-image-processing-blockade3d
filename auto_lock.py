"""
Auto Lock-On - Automatically locks on nearest target when shooting
Ultra-Safe: All anti-cheat protections applied
"""
import math
import random
import time
import numpy as np
import cv2
import pyautogui
from grabscreen import grab_screen
from window_finder import window_finder
import config


class AutoLockOn:
    """
    Auto Lock-On: Automatically locks on nearest target when left-clicking
    Ultra-Safe: Uses all anti-cheat protections
    """
    
    def __init__(self):
        self.enabled = False
        self.last_lock_time = 0
        self.lock_cooldown = 0.3  # Minimum time between auto-locks (300ms)
        
    def find_nearest_target(self, screen, whiteChannel, current_x, current_y):
        """
        Find nearest target to current mouse position
        Returns (target_x, target_y, color) or None
        """
        best_target = None
        best_distance = float('inf')
        
        # Search in ROI for targets
        iix = 168  # Start from top of ROI
        iiy = 0
        intSubdiv = config.INT_SUBDIV
        
        # Convert screen coordinates to game coordinates
        if config.AUTO_DETECT_WINDOW:
            game_region = window_finder.get_game_region()
            if game_region:
                window_left, window_top, _, _ = game_region
                game_x = current_x - window_left
                game_y = current_y - window_top
            else:
                game_x = current_x
                game_y = current_y - config.SCREEN_OFFSET_Y
        else:
            game_x = current_x
            game_y = current_y - config.SCREEN_OFFSET_Y
        
        # Search for targets near current position
        search_radius = 150  # Search within 150 pixels
        min_x = max(0, int(game_y - search_radius))
        max_x = min(config.SCREEN_HEIGHT, int(game_y + search_radius))
        min_y = max(0, int(game_x - search_radius))
        max_y = min(config.SCREEN_WIDTH, int(game_x + search_radius))
        
        # Scan for targets
        for x in range(min_x, max_x, intSubdiv):
            for y in range(min_y, max_y, intSubdiv):
                if whiteChannel[x, y] == 255:
                    # Check if it's a player color
                    if 0 <= x < screen.shape[0] and 0 <= y < screen.shape[1]:
                        pixel = screen[x, y]
                        r, g, b = pixel[0], pixel[1], pixel[2]
                        
                        detected_color = None
                        if r == 255 and g < config.COLOR_THRESHOLD and b < config.COLOR_THRESHOLD:
                            detected_color = 'red'
                        elif r < config.COLOR_THRESHOLD and g == 255 and b < config.COLOR_THRESHOLD:
                            detected_color = 'green'
                        elif r < config.COLOR_THRESHOLD and g < config.COLOR_THRESHOLD and b == 255:
                            detected_color = 'blue'
                        
                        if detected_color:
                            # Calculate distance to current position
                            distance = math.sqrt((x - game_y)**2 + (y - game_x)**2)
                            
                            # Prefer closer targets
                            if distance < best_distance:
                                best_distance = distance
                                # Target head (slightly above)
                                head_offset = -15  # 15 pixels up for head
                                best_target = (x + head_offset, y, detected_color)
        
        return best_target
    
    def auto_lock_on_shot(self, screen, whiteChannel):
        """
        Automatically lock on nearest target when shooting
        Returns locked target or None
        """
        if not self.enabled:
            return None
        
        # Cooldown check
        current_time = time.time()
        if current_time - self.last_lock_time < self.lock_cooldown:
            return None
        
        # Get current mouse position
        current_x, current_y = pyautogui.position()
        
        # Find nearest target
        target = self.find_nearest_target(screen, whiteChannel, current_x, current_y)
        
        if target:
            self.last_lock_time = current_time
            # Ultra-Safe: Random cooldown variation
            self.lock_cooldown = 0.3 * random.uniform(0.8, 1.3)
            return target
        
        return None


# Global instance
auto_lock = AutoLockOn()

