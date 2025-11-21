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
    mid_x = (start_x + end_x) / 2
    mid_y = (start_y + end_y) / 2
    
    # Add random offset to control point for natural curve
    offset_range = distance * random.uniform(0.08, 0.15)  # More variation
    cp_x = mid_x + random.uniform(-offset_range, offset_range)
    cp_y = mid_y + random.uniform(-offset_range, offset_range)
    
    # Sometimes add overshoot for more human-like behavior
    if add_overshoot and random.random() < 0.2:  # 20% chance
        overshoot_factor = random.uniform(1.05, 1.15)
        end_x = start_x + (end_x - start_x) * overshoot_factor
        end_y = start_y + (end_y - start_y) * overshoot_factor
    
    # Generate movement points
    steps = max(5, int(duration * 60))  # ~60 steps per second
    points = []
    
    for i in range(steps + 1):
        t = i / steps
        # Ease-in-out curve for natural acceleration/deceleration
        eased_t = t * t * (3 - 2 * t)
        
        x = bezier_curve(start_x, cp_x, end_x, eased_t)
        y = bezier_curve(start_y, cp_y, end_y, eased_t)
        
        # Add small random jitter (imperfection) - more variation
        jitter_x = random.uniform(-1.0, 1.0)
        jitter_y = random.uniform(-1.0, 1.0)
        x += jitter_x
        y += jitter_y
        
        # Add micro-tremor (very small human hand tremor)
        tremor = random.uniform(-0.3, 0.3)
        x += tremor
        y += tremor
        
        # Variable delay per step (more human-like)
        base_delay = duration / steps
        # Add small random variation to each step delay
        delay = base_delay * random.uniform(0.9, 1.1)
        points.append((int(x), int(y), delay))
    
    return points


def add_aim_imperfection(target_x, target_y, accuracy=0.95):
    """
    Add small random offset to aim point to simulate human imperfection
    
    Args:
        target_x, target_y: Perfect aim coordinates
        accuracy: Accuracy factor (0.0-1.0), higher = more accurate
    
    Returns:
        (x, y) tuple with slight imperfection
    """
    # Calculate max offset based on accuracy
    max_offset = (1.0 - accuracy) * 10  # Max 10 pixels at 0% accuracy
    
    offset_x = random.uniform(-max_offset, max_offset)
    offset_y = random.uniform(-max_offset, max_offset)
    
    return (int(target_x + offset_x), int(target_y + offset_y))


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

