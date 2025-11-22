"""
Aimbot Controller - Integrates GUI with main aimbot functionality
Handles right-click lock-on and target detection
"""
import threading
import time
import math
import random
import numpy as np
import cv2
import pyautogui
from grabscreen import grab_screen
from keys import Keys
from mouse_utils import human_like_mouse_move, add_aim_imperfection, random_delay
from window_finder import window_finder
from anti_cheat import anti_cheat
import config


class AimbotController:
    def __init__(self, gui=None):
        self.gui = gui
        self.keys = Keys()
        self.running = False
        self.locked_target = None
        self.lock_on_active = False
        
    def find_target_head(self, screen, whiteChannel, start_x, start_y, search_radius=50):
        """
        Find the head/upper body of a target near the given coordinates
        Looks for white pixels (outline) with colored pixels inside (player)
        """
        best_target = None
        best_score = 0
        
        # Search in a radius around the click point
        for dy in range(-search_radius, search_radius, 5):
            for dx in range(-search_radius, search_radius, 5):
                y = start_y + dy
                x = start_x + dx
                
                # Check bounds
                if not (0 <= x < config.SCREEN_HEIGHT and 0 <= y < config.SCREEN_WIDTH):
                    continue
                    
                # Check if there's a white outline (target border)
                if whiteChannel[x, y] == 255:
                    # Check surrounding area for player color
                    color_score = 0
                    head_y = x - 10  # Look slightly above for head
                    
                    if 0 <= head_y < config.SCREEN_HEIGHT:
                        # Check for colored pixels (player)
                        for check_y in range(max(0, y-5), min(config.SCREEN_WIDTH, y+5)):
                            pixel = screen[head_y, check_y]
                            if self.is_player_color(pixel):
                                color_score += 1
                                
                    # Prefer targets with more color pixels (more likely to be a player)
                    if color_score > best_score:
                        best_score = color_score
                        best_target = (x, y)
                        
        return best_target
        
    def is_player_color(self, pixel):
        """Check if pixel is a player color (red, green, or blue)"""
        r, g, b = pixel[0], pixel[1], pixel[2]
        
        if (r == 255 and g < config.COLOR_THRESHOLD and b < config.COLOR_THRESHOLD):
            return True
        if (r < config.COLOR_THRESHOLD and g == 255 and b < config.COLOR_THRESHOLD):
            return True
        if (r < config.COLOR_THRESHOLD and g < config.COLOR_THRESHOLD and b == 255):
            return True
        return False
        
    def lock_on_to_position(self, screen_x, screen_y):
        """
        Lock on to target at screen coordinates
        Converts screen coords to game coords and finds nearest target head
        """
        # Convert screen coordinates to game coordinates
        game_x = screen_x
        game_y = screen_y - config.SCREEN_OFFSET_Y
        
        if not (0 <= game_x < config.SCREEN_WIDTH and 0 <= game_y < config.SCREEN_HEIGHT):
            return None
            
        # Capture screen to find target (2025 - auto-detect window)
        if config.AUTO_DETECT_WINDOW:
            game_region = window_finder.get_game_region()
            if game_region:
                left, top, width, height = game_region
                screen = grab_screen(region=(left, top, left + width, top + height), use_window_finder=True)
            else:
                screen = grab_screen(region=(0, config.SCREEN_OFFSET_Y, 
                                            config.SCREEN_WIDTH, 
                                            config.SCREEN_HEIGHT + config.SCREEN_OFFSET_Y), use_window_finder=False)
        else:
            screen = grab_screen(region=(0, config.SCREEN_OFFSET_Y, 
                                        config.SCREEN_WIDTH, 
                                        config.SCREEN_HEIGHT + config.SCREEN_OFFSET_Y), use_window_finder=False)
        
        # Apply ROI mask
        vertices = np.array(config.ROI_VERTICES, np.int32)
        mask = np.zeros_like(screen)
        cv2.fillConvexPoly(mask, vertices, 255)
        screen = np.bitwise_and(screen, mask)
        
        # Convert to grayscale and threshold
        screenGray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        ret, whiteChannel = cv2.threshold(screenGray, config.THRESHOLD_VALUE, 255, cv2.THRESH_BINARY)
        
        # Find target head near click position
        target = self.find_target_head(screen, whiteChannel, game_y, game_x)
        
        if target:
            self.locked_target = target
            self.lock_on_active = True
            return target
        else:
            # If no target found, use click position as lock point
            self.locked_target = (game_y, game_x)
            self.lock_on_active = True
            return self.locked_target
            
    def maintain_lock(self):
        """Maintain lock on target - continuously aim at locked position"""
        if not self.lock_on_active or self.locked_target is None:
            return
            
        current_x, current_y = pyautogui.position()
        
        # Convert game coordinates to screen coordinates (2025 - fullscreen support)
        target_game_y, target_game_x = self.locked_target
        
        # Get window position for accurate coordinates
        if config.AUTO_DETECT_WINDOW:
            game_region = window_finder.get_game_region()
            if game_region:
                window_left, window_top, window_width, window_height = game_region
                target_screen_x = window_left + target_game_x
                target_screen_y = window_top + target_game_y
            else:
                target_screen_x = target_game_x
                target_screen_y = target_game_y + config.SCREEN_OFFSET_Y
        else:
            target_screen_x = target_game_x
            target_screen_y = target_game_y + config.SCREEN_OFFSET_Y
        
        # Calculate offset
        offset_x = target_screen_x - current_x
        offset_y = target_screen_y - current_y
        
        distance = math.sqrt(offset_x**2 + offset_y**2)
        
        # Only move if target is reasonably close and not already locked
        if distance < config.MAX_AIM_DISTANCE and distance > 2:
            # Use human-like movement for smooth tracking
            movement_points = human_like_mouse_move(
                current_x, current_y, 
                target_screen_x, target_screen_y,
                duration=min(0.1, distance / 600),  # Faster for tracking
                control_points=1
            )
            
            # Execute movement (limit steps for smooth tracking)
            for mx, my, delay in movement_points[:2]:
                rel_dx = mx - current_x
                rel_dy = my - current_y
                
                if abs(rel_dx) > 0 or abs(rel_dy) > 0:
                    self.keys.directMouse(dx=rel_dx, dy=rel_dy, buttons=0)
                    current_x, current_y = mx, my
                    time.sleep(delay)
                    
    def aim_at_target(self, target_x, target_y, shoot=False):
        """
        Aim at target with human-like movement
        """
        current_x, current_y = pyautogui.position()
        
        # Add imperfection
        target_x, target_y = add_aim_imperfection(
            target_x, target_y, 
            accuracy=config.AIM_ACCURACY
        )
        
        # Calculate relative movement
        offset_x = target_x - current_x
        offset_y = target_y - current_y
        
        distance = math.sqrt(offset_x**2 + offset_y**2)
        
        if distance < config.MAX_AIM_DISTANCE:
            # Human-like movement
            movement_points = human_like_mouse_move(
                current_x, current_y, 
                target_x, target_y,
                duration=None,
                control_points=1
            )
            
            # Execute movement
            for mx, my, delay in movement_points:
                rel_dx = mx - current_x
                rel_dy = my - current_y
                
                if abs(rel_dx) > 0 or abs(rel_dy) > 0:
                    self.keys.directMouse(dx=rel_dx, dy=rel_dy, buttons=0)
                    current_x, current_y = mx, my
                    time.sleep(delay)
                    
            # Shoot if requested
            if shoot:
                time.sleep(random_delay(config.MIN_REACTION_TIME_MS, config.MAX_REACTION_TIME_MS))
                self.keys.directMouse(dx=0, dy=0, buttons=self.keys.mouse_lb_press)
                time.sleep(random.uniform(config.MIN_SHOOT_HOLD_MS/1000.0, 
                                         config.MAX_SHOOT_HOLD_MS/1000.0))
                self.keys.directMouse(dx=0, dy=0, buttons=self.keys.mouse_lb_release)
                time.sleep(random_delay(config.POST_SHOOT_DELAY_MIN_MS, 
                                      config.POST_SHOOT_DELAY_MAX_MS))

