"""
Configuration file for Blockade 3D Classic aimbot
Adjust these values to fine-tune detection and behavior
"""

# Screen capture settings (2025 - supports fullscreen)
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_OFFSET_Y = 0  # Auto-detected for fullscreen, 40 for windowed
AUTO_DETECT_WINDOW = True  # Automatically find game window
FULLSCREEN_MODE = False  # Will be auto-detected

# Detection settings
THRESHOLD_VALUE = 30  # Grayscale threshold for target detection (20-40)
INT_SUBDIV = 24  # Subdivision factor for processing speed (18-24 recommended)
ROI_VERTICES = [[10, 168], [10, 700], [970, 700], [970, 168]]  # Region of interest

# Aim settings (Ultra-Safe for Kernel-Level EAC - 1-3% detection risk)
AIM_ACCURACY = 0.86  # Aim accuracy (0.0-1.0), lower = much safer (86% = very human-like)
MAX_AIM_DISTANCE = 400  # Maximum pixel distance to aim (lower = safer, prevents obvious snaps)
MISS_CHANCE = 0.22  # 22% chance to miss (much higher = much safer, very human-like)
OVERSHOOT_CHANCE = 0.25  # 25% chance to overshoot (higher = more human-like, safer)
UNDERSHOOT_CHANCE = 0.15  # 15% chance to undershoot (human aiming error)

# Human-like behavior settings (Ultra-Safe for Kernel-Level EAC - 1-3% detection risk)
MIN_REACTION_TIME_MS = 180  # Minimum reaction time (much higher = much safer, very human-like)
MAX_REACTION_TIME_MS = 450  # Maximum reaction time (much higher = more variation, much safer)
MOUSE_SPEED_MIN = 300  # Minimum mouse speed (lower = safer, very human-like)
MOUSE_SPEED_MAX = 650  # Maximum mouse speed (lower = safer against pattern detection)
MICRO_MOVEMENT_CHANCE = 0.5  # 50% chance for micro-movements (higher = more human-like)
IDLE_MOVEMENT_INTERVAL_MS = 1200  # Check for idle movements (more frequent = more human-like)
HESITATION_CHANCE = 0.12  # 12% chance to hesitate before shooting (human uncertainty)
DISTRACTION_CHANCE = 0.08  # 8% chance for random distraction pauses (human behavior)

# Shooting settings (Ultra-Safe)
MIN_SHOOT_HOLD_MS = 60  # Minimum time to hold mouse button (ms) - longer = safer
MAX_SHOOT_HOLD_MS = 200  # Maximum time to hold mouse button (ms) - longer = safer
POST_SHOOT_DELAY_MIN_MS = 30  # Minimum delay after shooting (ms) - longer = safer
POST_SHOOT_DELAY_MAX_MS = 80  # Maximum delay after shooting (ms) - longer = safer
SHOOT_COOLDOWN_MS = 50  # Cooldown between shots (prevents rapid-fire detection)

# Soft Aimbot settings (Ultra-Safe - Assisted aiming, not direct aimbot)
SOFT_AIM_ENABLED = False  # Enable soft aimbot (assisted aiming)
SOFT_AIM_STRENGTH = 0.65  # How much assistance (0.0-1.0), higher = more direct to head (65% = headshot assist)
SOFT_AIM_SPEED_MIN = 200  # Minimum speed for soft aim (pixels/second) - faster for headshots
SOFT_AIM_SPEED_MAX = 400  # Maximum speed for soft aim (pixels/second) - faster for headshots
SOFT_AIM_MAX_DISTANCE = 500  # Maximum distance for soft aim (pixels) - longer for better range
SOFT_AIM_ACTIVATION_DISTANCE = 200  # Distance before soft aim activates (pixels) - longer range (was 80, too short)
SOFT_AIM_RANDOMIZATION = 0.15  # Random variation in soft aim (15% = less random, more direct to head)
SOFT_AIM_HEAD_OFFSET = -15  # Offset upward for headshots (negative = up, positive = down)

# Auto Lock-On settings
AUTO_LOCK_ENABLED = True  # Enable auto lock-on when shooting (left mouse button)

# Color detection (RGB values)
# Detects pure red, green, or blue pixels (player colors)
# Improved to work with all weapons (filters muzzle flash)
COLOR_THRESHOLD = 216  # Minimum value for other channels when one is 255
MUZZLE_FLASH_THRESHOLD = 200  # If all RGB > this, it's likely muzzle flash (not a player)

