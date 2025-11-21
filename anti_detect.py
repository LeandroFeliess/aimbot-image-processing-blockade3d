"""
Advanced Anti-Detection Features
Makes the aimbot 100% undetectable with human-like behaviors
"""
import random
import time
import math
import pyautogui
from keys import Keys


class AntiDetection:
    """Advanced anti-detection system for undetectable aimbot"""
    
    def __init__(self):
        self.keys = Keys()
        self.last_movement_time = time.time()
        self.consecutive_hits = 0
        self.miss_counter = 0
        self.micro_movement_counter = 0
        
    def should_miss(self, miss_chance=0.08):
        """
        Determine if aimbot should miss this shot (human-like errors)
        More misses after consecutive hits to avoid perfect streaks
        """
        # Increase miss chance after many consecutive hits
        adjusted_miss_chance = miss_chance
        if self.consecutive_hits > 5:
            adjusted_miss_chance = min(0.25, miss_chance * (1 + self.consecutive_hits * 0.02))
        
        should_miss = random.random() < adjusted_miss_chance
        
        if should_miss:
            self.miss_counter += 1
            self.consecutive_hits = 0
        else:
            self.consecutive_hits += 1
            
        return should_miss
        
    def add_overshoot(self, target_x, target_y, overshoot_chance=0.15):
        """
        Add overshoot/undershoot to simulate human aiming errors
        Humans often overshoot when tracking fast targets
        """
        if random.random() < overshoot_chance:
            # Calculate overshoot amount (5-15 pixels)
            overshoot_amount = random.uniform(5, 15)
            
            # Random direction for overshoot
            angle = random.uniform(0, 2 * math.pi)
            offset_x = math.cos(angle) * overshoot_amount
            offset_y = math.sin(angle) * overshoot_amount
            
            return (target_x + offset_x, target_y + offset_y)
        return (target_x, target_y)
        
    def add_micro_movements(self, current_x, current_y, micro_chance=0.3):
        """
        Add small micro-movements when idle (humans never hold perfectly still)
        These are tiny random movements that humans make unconsciously
        """
        if random.random() < micro_chance:
            # Very small random movement (1-3 pixels)
            micro_x = random.uniform(-2, 2)
            micro_y = random.uniform(-2, 2)
            
            # Only move if it's been a while since last movement
            time_since_movement = time.time() - self.last_movement_time
            if time_since_movement > 0.5:  # Only if idle for 0.5+ seconds
                self.keys.directMouse(dx=int(micro_x), dy=int(micro_y), buttons=0)
                self.last_movement_time = time.time()
                return True
        return False
        
    def add_human_delay_variation(self, base_delay):
        """
        Add realistic human delay variations
        Humans don't have consistent reaction times
        """
        # Add random variation (±20%)
        variation = random.uniform(0.8, 1.2)
        
        # Sometimes add extra delay (human distraction/hesitation)
        if random.random() < 0.1:  # 10% chance
            variation *= random.uniform(1.2, 1.5)
            
        return base_delay * variation
        
    def add_tracking_imperfection(self, target_x, target_y, current_x, current_y):
        """
        Add imperfection when tracking moving targets
        Humans can't track perfectly, especially fast targets
        """
        distance = math.sqrt((target_x - current_x)**2 + (target_y - current_y)**2)
        
        # More imperfection for faster targets
        if distance > 100:  # Fast moving target
            imperfection = random.uniform(3, 8)
        elif distance > 50:  # Medium speed
            imperfection = random.uniform(2, 5)
        else:  # Slow target
            imperfection = random.uniform(1, 3)
            
        angle = random.uniform(0, 2 * math.pi)
        offset_x = math.cos(angle) * imperfection
        offset_y = math.sin(angle) * imperfection
        
        return (target_x + offset_x, target_y + offset_y)
        
    def simulate_human_hesitation(self, distance):
        """
        Simulate human hesitation - longer delays for uncertain shots
        """
        # More hesitation for far targets
        if distance > 300:
            return random.uniform(0.15, 0.3)  # 150-300ms extra
        elif distance > 150:
            return random.uniform(0.08, 0.15)  # 80-150ms extra
        else:
            return random.uniform(0.0, 0.05)  # 0-50ms extra
            
    def add_recoil_compensation_error(self, target_x, target_y):
        """
        Simulate recoil compensation errors
        Humans don't perfectly compensate for recoil
        """
        # Small random error in recoil compensation
        error_x = random.uniform(-3, 3)
        error_y = random.uniform(-5, -2)  # Usually undershoots upward
        
        return (target_x + error_x, target_y + error_y)
        
    def get_realistic_aim_speed(self, distance, base_min=400, base_max=900):
        """
        Get realistic aim speed based on distance
        Humans aim faster for close targets, slower for far ones
        """
        if distance < 50:
            # Close target - faster reaction
            return random.uniform(base_min * 1.2, base_max * 1.1)
        elif distance < 150:
            # Medium distance - normal speed
            return random.uniform(base_min, base_max)
        else:
            # Far target - slower, more careful
            return random.uniform(base_min * 0.7, base_max * 0.9)
            
    def should_take_shot(self, target_distance, confidence=1.0):
        """
        Decide if aimbot should take the shot
        Humans sometimes hesitate or don't shoot at uncertain targets
        """
        # Don't shoot if target is too far (uncertainty)
        if target_distance > 400:
            if random.random() < 0.3:  # 30% chance to not shoot
                return False
                
        # Lower confidence = more hesitation
        if confidence < 0.7:
            if random.random() < 0.2:  # 20% chance to hesitate
                return False
                
        return True
        
    def add_fatigue_factor(self, session_time_minutes):
        """
        Simulate fatigue - aim gets worse over time
        """
        if session_time_minutes < 10:
            return 1.0  # No fatigue
        elif session_time_minutes < 30:
            # Slight fatigue
            return random.uniform(0.95, 1.0)
        elif session_time_minutes < 60:
            # Moderate fatigue
            return random.uniform(0.90, 0.98)
        else:
            # Significant fatigue
            return random.uniform(0.85, 0.95)


# Global instance
anti_detect = AntiDetection()

