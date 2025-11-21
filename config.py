"""
Configuration file for Blockade 3D Classic aimbot
Adjust these values to fine-tune detection and behavior
"""

# Screen capture settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_OFFSET_Y = 40  # Offset for window title bar

# Detection settings
THRESHOLD_VALUE = 30  # Grayscale threshold for target detection (20-40)
INT_SUBDIV = 24  # Subdivision factor for processing speed (18-24 recommended)
ROI_VERTICES = [[10, 168], [10, 700], [970, 700], [970, 168]]  # Region of interest

# Aim settings
AIM_ACCURACY = 0.94  # Aim accuracy (0.0-1.0), lower = more human-like (94% is realistic)
MAX_AIM_DISTANCE = 500  # Maximum pixel distance to aim (prevents obvious snaps)
MISS_CHANCE = 0.08  # 8% chance to miss completely (human-like error rate)
OVERSHOOT_CHANCE = 0.15  # 15% chance to overshoot target slightly

# Human-like behavior settings
MIN_REACTION_TIME_MS = 80  # Minimum reaction time in milliseconds (more realistic)
MAX_REACTION_TIME_MS = 250  # Maximum reaction time in milliseconds (more variation)
MOUSE_SPEED_MIN = 400  # Minimum mouse speed (pixels per second) - more variation
MOUSE_SPEED_MAX = 900  # Maximum mouse speed (pixels per second) - wider range
MICRO_MOVEMENT_CHANCE = 0.3  # 30% chance for small micro-movements when idle
IDLE_MOVEMENT_INTERVAL_MS = 2000  # Check for idle movements every 2 seconds

# Shooting settings
MIN_SHOOT_HOLD_MS = 50  # Minimum time to hold mouse button (ms)
MAX_SHOOT_HOLD_MS = 150  # Maximum time to hold mouse button (ms)
POST_SHOOT_DELAY_MIN_MS = 20  # Minimum delay after shooting (ms)
POST_SHOOT_DELAY_MAX_MS = 50  # Maximum delay after shooting (ms)

# Color detection (RGB values)
# Detects pure red, green, or blue pixels (player colors)
COLOR_THRESHOLD = 216  # Minimum value for other channels when one is 255

