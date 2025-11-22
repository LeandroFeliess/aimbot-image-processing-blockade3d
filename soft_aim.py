"""
Soft Aimbot - Assisted Aiming (Ultra-Safe)
Slowly moves mouse towards target instead of direct snapping
Much more subtle and undetectable than regular aimbot
"""
import random
import time
import math
import pyautogui
from keys import Keys
from mouse_utils import human_like_mouse_move, add_aim_imperfection
from anti_detect import anti_detect
from anti_cheat import anti_cheat
import config


class SoftAimbot:
    """
    Soft aimbot - Assisted aiming that slowly moves towards target
    Ultra-Safe: Uses all anti-cheat protections
    """
    
    def __init__(self):
        self.keys = Keys()
        self.last_soft_aim_time = 0
        self.soft_aim_cooldown = 0.05  # Minimum time between soft aim adjustments
        
    def soft_aim_towards_target(self, target_x, target_y, strength=None):
        """
        Soft aim: Slowly move mouse towards target (assisted aiming)
        Ultra-Safe: All anti-cheat protections applied
        
        Args:
            target_x, target_y: Target coordinates
            strength: How much assistance (0.0-1.0), None = use config
        """
        if strength is None:
            strength = config.SOFT_AIM_STRENGTH
        
        # Get current mouse position
        current_x, current_y = pyautogui.position()
        
        # Calculate distance to target
        dx = target_x - current_x
        dy = target_y - current_y
        distance = math.sqrt(dx**2 + dy**2)
        
        # Only activate if target is within activation distance
        if distance > config.SOFT_AIM_ACTIVATION_DISTANCE:
            # Debug: Print why it's not activating
            if random.random() < 0.1:  # 10% chance to print
                print(f"[SOFT AIM DEBUG] Target too far for activation: {distance} > {config.SOFT_AIM_ACTIVATION_DISTANCE}")
            return False
        
        # Only activate if target is within max distance
        if distance > config.SOFT_AIM_MAX_DISTANCE:
            # Debug: Print why it's not activating
            if random.random() < 0.1:  # 10% chance to print
                print(f"[SOFT AIM DEBUG] Target too far: {distance} > {config.SOFT_AIM_MAX_DISTANCE}")
            return False
        
        # Cooldown check (prevent too frequent adjustments)
        current_time = time.time()
        if current_time - self.last_soft_aim_time < self.soft_aim_cooldown:
            # Debug: Print why it's on cooldown
            if random.random() < 0.1:  # 10% chance to print
                time_since_last = current_time - self.last_soft_aim_time
                print(f"[SOFT AIM DEBUG] On cooldown: {time_since_last:.3f}s < {self.soft_aim_cooldown:.3f}s")
            return False
        
        # Ultra-Safe: Random cooldown variation (EAC can detect consistent timing)
        cooldown_variation = random.uniform(0.8, 1.3)
        self.soft_aim_cooldown = 0.05 * cooldown_variation
        
        # Calculate movement towards target HEAD (not body center)
        # Adjust target upward for headshots
        try:
            head_offset = config.SOFT_AIM_HEAD_OFFSET
        except:
            head_offset = -15  # Default: 15 pixels up for head
        
        # Move towards head (target + head offset)
        target_head_x = target_x
        target_head_y = target_y + head_offset
        
        # Calculate movement (more direct to head for headshots)
        dx_to_head = target_head_x - current_x
        dy_to_head = target_head_y - current_y
        
        move_x = dx_to_head * strength
        move_y = dy_to_head * strength
        
        # Less randomization for more direct headshots (but still some variation)
        random_factor = random.uniform(1.0 - config.SOFT_AIM_RANDOMIZATION, 
                                      1.0 + config.SOFT_AIM_RANDOMIZATION)
        move_x *= random_factor
        move_y *= random_factor
        
        # Less imperfection for headshots (more accurate)
        move_x, move_y = add_aim_imperfection(
            current_x + move_x,
            current_y + move_y,
            accuracy=0.95  # 95% accuracy for soft aim headshots (less error)
        )
        move_x -= current_x
        move_y -= current_y
        
        # Calculate target position
        target_soft_x = current_x + move_x
        target_soft_y = current_y + move_y
        
        # Ultra-Safe: Calculate speed based on distance (human-like)
        move_distance = math.sqrt(move_x**2 + move_y**2)
        if move_distance < 5:  # Too small movement, skip
            return False
        
        # Get realistic speed (slower for soft aim)
        base_speed = random.uniform(config.SOFT_AIM_SPEED_MIN, config.SOFT_AIM_SPEED_MAX)
        
        # Ultra-Safe: Variabele speed based on distance
        if move_distance < 20:
            speed = base_speed * random.uniform(0.8, 1.0)  # Slower for small movements
        elif move_distance < 50:
            speed = base_speed * random.uniform(0.9, 1.1)  # Normal
        else:
            speed = base_speed * random.uniform(1.0, 1.2)  # Slightly faster for larger
        
        # Calculate duration
        duration = max(0.1, min(0.4, move_distance / speed))  # 100-400ms
        
        # Ultra-Safe: Add random variation to duration
        duration *= random.uniform(0.85, 1.15)
        
        # Generate human-like movement path
        movement_points = human_like_mouse_move(
            current_x, current_y,
            target_soft_x, target_soft_y,
            duration=duration,
            control_points=1,
            min_speed=speed * 0.9,
            max_speed=speed * 1.1,
            add_overshoot=False  # No overshoot for soft aim (too obvious)
        )
        
        # Ultra-Safe: Sometimes skip movement (human hesitation)
        if random.random() < 0.15:  # 15% chance to skip
            self.last_soft_aim_time = current_time
            return False
        
        # Execute movement in small steps
        executed = False
        for x, y, delay in movement_points:
            rel_dx = x - current_x
            rel_dy = y - current_y
            
            # Only send movement if there's actual change
            if abs(rel_dx) > 0.5 or abs(rel_dy) > 0.5:
                self.keys.directMouse(dx=int(rel_dx), dy=int(rel_dy), buttons=0)
                current_x, current_y = x, y
                executed = True
                
                # Ultra-Safe: Add human delay variation
                delay = anti_detect.add_human_delay_variation(delay)
                
                # Ultra-Safe: EAC-safe delay
                delay = anti_cheat.randomize_timing(delay)
                time.sleep(delay)
        
        # Update last movement time
        if executed:
            self.last_soft_aim_time = current_time
            
            # Ultra-Safe: Random delay after soft aim (human behavior)
            post_delay = random.uniform(0.02, 0.08)  # 20-80ms
            post_delay = anti_cheat.randomize_timing(post_delay)
            time.sleep(post_delay)
        
        return executed


# Global instance
soft_aimbot = SoftAimbot()

