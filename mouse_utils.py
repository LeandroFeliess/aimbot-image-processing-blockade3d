"""
Human-like mouse movement utilities for undetectable aimbot
Uses bezier curves, variable speed, and random imperfections
"""
import random
import time
import math
import numpy as np


def bezier_curve(p0, p1, p2, t):
    """Calculate point on quadratic bezier curve"""
    return (1-t)**2 * p0 + 2*(1-t)*t * p1 + t**2 * p2


def human_like_mouse_move(start_x, start_y, end_x, end_y, duration=None, control_points=1, 
                          min_speed=500, max_speed=800, add_overshoot=False):
    """
    Generate human-like mouse movement path using bezier curves
    
    Args:
        start_x, start_y: Starting position
        end_x, end_y: Target position
        duration: Movement duration in seconds (auto-calculated if None)
        control_points: Number of control points for bezier curve (1-3)
        min_speed: Minimum mouse speed (pixels per second)
        max_speed: Maximum mouse speed (pixels per second)
    
    Returns:
        List of (x, y, delay) tuples for smooth movement
    """
    try:
        import config
        min_speed = config.MOUSE_SPEED_MIN
        max_speed = config.MOUSE_SPEED_MAX
    except:
        pass
    
    distance = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
    
    # Auto-calculate duration based on distance (human-like: ~100-300ms for small moves)
    if duration is None:
        # Base speed with variation
        base_speed = random.uniform(min_speed, max_speed)
        duration = max(0.05, min(0.3, distance / base_speed))
        # Add random variation
        duration *= random.uniform(0.8, 1.2)
    
    # Generate control point(s) for bezier curve
    # Ultra-Safe: Meer chaos in control points (EAC detecteert te wiskundige berekeningen)
    mid_x = (start_x + end_x) / 2
    mid_y = (start_y + end_y) / 2
    
    # Add random offset to control point for natural curve (meer variatie)
    offset_range = distance * random.uniform(0.1, 0.2)  # Meer variatie (was 0.08-0.15)
    
    # Soms gebruik een compleet andere control point (meer chaos)
    if random.random() < 0.2:  # 20% kans op chaotische control point
        # Gebruik een willekeurige control point (meer chaos)
        cp_x = start_x + random.uniform(-distance * 0.3, distance * 0.3)
        cp_y = start_y + random.uniform(-distance * 0.3, distance * 0.3)
    else:
        # Normale control point met variatie
        cp_x = mid_x + random.uniform(-offset_range, offset_range)
        cp_y = mid_y + random.uniform(-offset_range, offset_range)
    
    # Add extra chaos factor (echte mensen hebben meer variatie)
    cp_x += random.uniform(-distance * 0.05, distance * 0.05)
    cp_y += random.uniform(-distance * 0.05, distance * 0.05)
    
    # Sometimes add overshoot for more human-like behavior
    if add_overshoot and random.random() < 0.2:  # 20% chance
        overshoot_factor = random.uniform(1.05, 1.15)
        end_x = start_x + (end_x - start_x) * overshoot_factor
        end_y = start_y + (end_y - start_y) * overshoot_factor
    
    # Generate movement points
    # Ultra-Safe: Variabele steps per second (50-70) om detecteerbare patronen te voorkomen
    steps_per_second = random.uniform(50, 70)  # Variabele in plaats van vaste 60
    steps = max(5, int(duration * steps_per_second))
    points = []
    
    # Ultra-Safe: Variabele easing curve (niet altijd perfect wiskundig)
    # EAC detecteert perfecte wiskundige curves - we variëren de easing
    use_perfect_easing = random.random() < 0.7  # 70% perfect, 30% imperfect
    if use_perfect_easing:
        easing_type = random.choice(['ease_in_out', 'ease_in', 'ease_out', 'linear'])
    else:
        easing_type = 'chaotic'  # Meer chaos zoals echte mensen
    
    for i in range(steps + 1):
        t = i / steps
        
        # Ultra-Safe: Variabele easing curves (EAC detecteert perfecte curves)
        if easing_type == 'ease_in_out':
            eased_t = t * t * (3 - 2 * t)  # Standaard ease-in-out
        elif easing_type == 'ease_in':
            eased_t = t * t  # Ease-in
        elif easing_type == 'ease_out':
            eased_t = 1 - (1 - t) * (1 - t)  # Ease-out
        elif easing_type == 'linear':
            eased_t = t  # Lineair
        else:  # chaotic - meer chaos zoals echte mensen
            # Imperfecte curve met meer variatie
            eased_t = t * t * (3 - 2 * t)  # Base curve
            eased_t += random.uniform(-0.1, 0.1) * t * (1 - t)  # Chaos factor
            eased_t = max(0, min(1, eased_t))  # Clamp
        
        # Add extra chaos factor (echte mensen hebben meer variatie)
        if random.random() < 0.15:  # 15% kans op extra chaos
            eased_t += random.uniform(-0.05, 0.05)
            eased_t = max(0, min(1, eased_t))
        
        x = bezier_curve(start_x, cp_x, end_x, eased_t)
        y = bezier_curve(start_y, cp_y, end_y, eased_t)
        
        # Ultra-Safe: Meer jitter en tremor (echte mensen hebben meer variatie)
        jitter_x = random.uniform(-1.5, 1.5)  # Meer variatie
        jitter_y = random.uniform(-1.5, 1.5)
        x += jitter_x
        y += jitter_y
        
        # Add micro-tremor (very small human hand tremor) - meer variatie
        tremor = random.uniform(-0.5, 0.5)  # Meer tremor
        x += tremor
        y += tremor
        
        # Ultra-Safe: Variabele step sizes (EAC detecteert te consistente steps)
        # Soms grotere steps, soms kleinere (echte mensen hebben variatie)
        step_size_multiplier = random.uniform(0.7, 1.3)  # Variabele step sizes
        base_delay = (duration / steps) * step_size_multiplier
        
        # Add small random variation to each step delay (meer variatie)
        delay = base_delay * random.uniform(0.85, 1.15)  # Meer variatie (was 0.9-1.1)
        
        # Ultra-Safe: Soms skip een step (echte mensen hebben onregelmatigheden)
        if random.random() < 0.05:  # 5% kans om step over te slaan
            delay *= random.uniform(1.5, 2.5)  # Langere delay = skip effect
        
        points.append((int(x), int(y), delay))
    
    return points


def add_aim_imperfection(target_x, target_y, accuracy=0.86):
    """
    Add random offset to aim point to simulate human imperfection (Ultra-Safe Mode)
    
    Args:
        target_x, target_y: Perfect aim coordinates
        accuracy: Accuracy factor (0.0-1.0), higher = more accurate
    
    Returns:
        (x, y) tuple with imperfection
    """
    # Calculate max offset based on accuracy (more imperfection for lower accuracy)
    max_offset = (1.0 - accuracy) * 18  # Max 18 pixels at 0% accuracy (wider range)
    
    # Add base offset
    offset_x = random.uniform(-max_offset, max_offset)
    offset_y = random.uniform(-max_offset, max_offset)
    
    # Add additional random jitter (human hand tremor)
    jitter_x = random.uniform(-3, 3)
    jitter_y = random.uniform(-3, 3)
    
    # Sometimes add larger error (human bad aim moments)
    if random.random() < 0.2:  # 20% chance
        error_x = random.uniform(-6, 6)
        error_y = random.uniform(-6, 6)
        offset_x += error_x
        offset_y += error_y
    
    return (int(target_x + offset_x + jitter_x), int(target_y + offset_y + jitter_y))


def random_delay(min_ms=None, max_ms=None):
    """Generate random delay in seconds"""
    try:
        import config
        if min_ms is None:
            min_ms = config.MIN_REACTION_TIME_MS
        if max_ms is None:
            max_ms = config.MAX_REACTION_TIME_MS
    except:
        if min_ms is None:
            min_ms = 5
        if max_ms is None:
            max_ms = 25
    return random.uniform(min_ms / 1000.0, max_ms / 1000.0)

