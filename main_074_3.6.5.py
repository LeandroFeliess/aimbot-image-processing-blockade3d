
import numpy as np
import cv2
import time
import random
import math
import pyautogui
import threading
from grabscreen import grab_screen
from keys import Keys
from mouse_utils import human_like_mouse_move, add_aim_imperfection, random_delay
from aimbot_controller import AimbotController
from anti_detect import anti_detect
from anti_cheat import anti_cheat
from window_finder import window_finder
from soft_aim import soft_aimbot
from wallhacks import wallhacks
from auto_lock import auto_lock
import config

#import playsound

import keyboard


#multiprocessor
# from multiprocessing import Pool


# for stastical analisys
import matplotlib.pyplot as plt

# file name
import os

stats = []

st_total_time = time.time()

# Use config values
HEIGTH = config.SCREEN_HEIGHT
WIDTH = config.SCREEN_WIDTH

keys = Keys()

#tips for speed:
#use it from the windows explorer
#during the screengrab versuss the
#offset of the coordinates calculated for the aiming part

stopScript = False

# the first:BLUE?
# the second:GREEN
# the third:RED?
# yellow
# red [255   0   0]
# green [  0 255  0]
# blue [  0   0 255]
# dropped idea for now
def is_a_RelevantColor(tmpScreenRGBpixel):
    """
    Check if pixel is a player color (red, green, or blue)
    Improved to work with all weapons including muzzle flash
    """
    # Extract RGB values
    r, g, b = tmpScreenRGBpixel[0], tmpScreenRGBpixel[1], tmpScreenRGBpixel[2]
    
    # Filter out muzzle flash: muzzle flash is usually very bright/white
    # If all channels are high, it's likely muzzle flash, not a player
    try:
        muzzle_threshold = config.MUZZLE_FLASH_THRESHOLD
    except:
        muzzle_threshold = 200  # Fallback
    
    if r > muzzle_threshold and g > muzzle_threshold and b > muzzle_threshold:
        return False  # Likely muzzle flash (white/bright)
    
    # Check for pure red player (R=255, G and B low)
    if (r == 255) and (g < config.COLOR_THRESHOLD) and (b < config.COLOR_THRESHOLD):
        return True
    
    # Check for pure green player (G=255, R and B low)
    if (r < config.COLOR_THRESHOLD) and (g == 255) and (b < config.COLOR_THRESHOLD):
        return True
    
    # Check for pure blue player (B=255, R and G low)
    if (r < config.COLOR_THRESHOLD) and (g < config.COLOR_THRESHOLD) and (b == 255):
        return True
    
    return False

## 10 0 right
##-10 0 left
#   0 10 down
#   0 -10 up
def mouse_shoot(click_x, click_y):
    """
    Human-like mouse movement with bezier curves and imperfections
    100% undetectable aimbot with advanced anti-detection
    """
    # Check if should miss (human-like errors - ultra-safe mode)
    if anti_detect.should_miss(config.MISS_CHANCE):
        # Miss intentionally - aim significantly off target (more realistic)
        miss_offset = random.uniform(20, 40)  # Miss by 20-40 pixels (wider range)
        angle = random.uniform(0, 2 * math.pi)
        click_x += math.cos(angle) * miss_offset
        click_y += math.sin(angle) * miss_offset
        
        # Sometimes miss by even more (human completely misses)
        if random.random() < 0.3:  # 30% chance
            miss_offset = random.uniform(40, 60)
            click_x += math.cos(angle) * miss_offset * 0.5
            click_y += math.sin(angle) * miss_offset * 0.5
    
    # Get current mouse position
    current_x, current_y = pyautogui.position()
    
    # Calculate target
    target_x = current_x + click_x
    target_y = current_y + click_y
    
    # Add overshoot chance
    target_x, target_y = anti_detect.add_overshoot(target_x, target_y, config.OVERSHOOT_CHANCE)
    
    # Add imperfection to aim (ultra-safe mode - more imperfection)
    target_x, target_y = add_aim_imperfection(
        target_x, 
        target_y, 
        accuracy=config.AIM_ACCURACY
    )
    
    # Additional random error (human uncertainty)
    if random.random() < 0.15:  # 15% chance for extra error
        error_x = random.uniform(-4, 4)
        error_y = random.uniform(-4, 4)
        target_x += error_x
        target_y += error_y
    
    # Calculate distance for speed adjustment
    distance = math.sqrt(click_x**2 + click_y**2)
    
    # Get realistic speed based on distance
    realistic_speed = anti_detect.get_realistic_aim_speed(distance, 
                                                          config.MOUSE_SPEED_MIN, 
                                                          config.MOUSE_SPEED_MAX)
    
    # Ultra-Safe: Soms maak een "slechte" beweging (echte mensen maken fouten)
    # EAC detecteert te perfecte bewegingen - we simuleren menselijke fouten
    make_bad_movement = random.random() < 0.12  # 12% kans op slechte beweging
    
    if make_bad_movement:
        # Simuleer slechte beweging: te ver, te kort, of verkeerde richting
        bad_movement_type = random.choice(['overshoot', 'undershoot', 'wrong_direction'])
        
        if bad_movement_type == 'overshoot':
            # Te ver - overshoot doel
            overshoot_factor = random.uniform(1.15, 1.35)
            target_x = current_x + (target_x - current_x) * overshoot_factor
            target_y = current_y + (target_y - current_y) * overshoot_factor
        elif bad_movement_type == 'undershoot':
            # Te kort - kom niet helemaal bij doel
            undershoot_factor = random.uniform(0.65, 0.85)
            target_x = current_x + (target_x - current_x) * undershoot_factor
            target_y = current_y + (target_y - current_y) * undershoot_factor
        else:  # wrong_direction
            # Verkeerde richting - kleine offset
            angle_error = random.uniform(-0.3, 0.3)  # Radians
            distance = math.sqrt((target_x - current_x)**2 + (target_y - current_y)**2)
            current_angle = math.atan2(target_y - current_y, target_x - current_x)
            target_x = current_x + math.cos(current_angle + angle_error) * distance * 0.7
            target_y = current_y + math.sin(current_angle + angle_error) * distance * 0.7
    
    # Use human-like movement path with overshoot option
    movement_points = human_like_mouse_move(
        current_x, current_y, 
        target_x, target_y,
        duration=None,  # Auto-calculate
        control_points=1,
        min_speed=realistic_speed * 0.9,
        max_speed=realistic_speed * 1.1,
        add_overshoot=(random.random() < config.OVERSHOOT_CHANCE)
    )
    
    # Execute movement in small steps
    # Ultra-Safe: Soms skip movements, soms extra movements (EAC detecteert te regelmatige frequency)
    step_skip_chance = 0.08  # 8% kans om een step over te slaan (echte mensen hebben onregelmatigheden)
    step_extra_chance = 0.05  # 5% kans op extra micro-movement
    
    for i, (x, y, delay) in enumerate(movement_points):
        # Ultra-Safe: Soms skip een step (echte mensen hebben onregelmatigheden)
        if random.random() < step_skip_chance:
            # Skip deze step - langere delay
            delay *= random.uniform(1.5, 2.0)
            time.sleep(delay)
            continue
        
        rel_dx = x - current_x
        rel_dy = y - current_y
        
        # Only send movement if there's actual change
        if abs(rel_dx) > 0 or abs(rel_dy) > 0:
            keys.directMouse(dx=rel_dx, dy=rel_dy, buttons=0)
            current_x, current_y = x, y
            
            # Ultra-Safe: Soms extra micro-movement (echte mensen hebben kleine extra bewegingen)
            if random.random() < step_extra_chance:
                # Kleine extra beweging (echte mensen hebben tremor)
                micro_dx = random.uniform(-0.5, 0.5)
                micro_dy = random.uniform(-0.5, 0.5)
                keys.directMouse(dx=int(micro_dx), dy=int(micro_dy), buttons=0)
            
            # Add human delay variation
            delay = anti_detect.add_human_delay_variation(delay)
            time.sleep(delay)
    
    # Add extensive hesitation for uncertain shots (ultra-safe mode)
    hesitation = anti_detect.simulate_human_hesitation(distance)
    # Add extra hesitation factor
    hesitation *= random.uniform(1.2, 1.8)  # More hesitation
    time.sleep(hesitation)
    
    # Sometimes add extra pause (human needs to think)
    try:
        if random.random() < config.HESITATION_CHANCE:
            extra_pause = random.uniform(0.1, 0.3)
            time.sleep(extra_pause)
    except:
        if random.random() < 0.12:  # Fallback
            extra_pause = random.uniform(0.1, 0.3)
            time.sleep(extra_pause)
    
    # Sometimes add distraction pause (human gets distracted)
    try:
        if random.random() < config.DISTRACTION_CHANCE:
            distraction = random.uniform(0.15, 0.4)
            time.sleep(distraction)
    except:
        if random.random() < 0.08:  # Fallback
            distraction = random.uniform(0.15, 0.4)
            time.sleep(distraction)
    
    # Small random delay before shooting (with variation)
    base_delay = random_delay(config.MIN_REACTION_TIME_MS, config.MAX_REACTION_TIME_MS)
    delay = anti_detect.add_human_delay_variation(base_delay)
    time.sleep(delay)
    
    # AUTO LOCK-ON: When shooting (left mouse button), auto-lock on nearest target
    # Note: screen and whiteChannel are captured in main loop, not in mouse_shoot
    # Auto lock-on is handled in main loop when target is detected
    
    # Press and release with human-like timing
    keys.directMouse(dx=0, dy=0, buttons=keys.mouse_lb_press)
    hold_time = random.uniform(config.MIN_SHOOT_HOLD_MS/1000.0, config.MAX_SHOOT_HOLD_MS/1000.0)
    hold_time *= anti_detect.add_human_delay_variation(1.0)  # Add variation
    time.sleep(hold_time)
    keys.directMouse(dx=0, dy=0, buttons=keys.mouse_lb_release)
    
    # Small delay after shooting
    post_delay = random_delay(config.POST_SHOOT_DELAY_MIN_MS, config.POST_SHOOT_DELAY_MAX_MS)
    post_delay *= anti_detect.add_human_delay_variation(1.0)
    time.sleep(post_delay)
    
    # Update last movement time for micro-movements
    anti_detect.last_movement_time = time.time()

#use by the windows settings
def nothing(x):
    pass

def roi(img, vertices):
    #blank mask:
    mask = np.zeros_like(img)
    #filling pixels inside the polygon defined by "vertices" with the fill color
    cv2.fillPoly(mask, vertices, 255)
    masked = np.bitwise_and(img, mask)
    return masked

def roi_color(img, vertices):
    #blank mask:
    mask = np.zeros_like(img)
    #filling pixels inside the polygon defined by "vertices" with the fill color
    cv2.fillPoly(mask, vertices, 255)
    np.set_printoptions(legacy=False)
    #extracting the first dimension
    a = np.dsplit(mask, 3)
    mask = np.dstack((a[0],a[0],a[0]))
    #applying the mask
    masked = np.bitwise_and(img, mask)
    return masked


# fillConvexPoly

def roi_fillConvexPoly(img, vertices):
    #blank mask:
    mask = np.zeros_like(img)
    #filling pixels inside the polygon defined by "vertices" with the fill color
    cv2.fillConvexPoly(mask, vertices, 255)
    masked = np.bitwise_and(img, mask)
    return masked


def multiproc_target_finding(x):
    # todo
    # time.sleep(1)
    # print("slept for 1 sec")
    print(str(x))
    return True

for i in list(range(4))[::-1]:
    print(i+1)
    time.sleep(1)

last_time = time.time()

DEBUG = 0
DEBUGwhiteGray = 1

toolDEBUG = 0

boolMoveMouse = 0
boolMoveSlowMouse = 0

boolMat = 0
##24 ok
#18 ok pebkac and drunk
# intSubdiv = 18
# intSubdiv = 18
# intSubdiv = 24 v65 
intSubdiv = config.INT_SUBDIV
#bugfix missing last lines
iHEIGTH = (HEIGTH//intSubdiv)
iWIDTH = (WIDTH//intSubdiv)
#bugfix inverted width height
simpleMat = np.zeros((iHEIGTH,iWIDTH,1), np.uint8)

boolDisableMask = 0

img = np.zeros((50,400,3), np.uint8)
cv2.namedWindow('settings')
# create trackbars for color change
cv2.createTrackbar('0..255Low','settings',0,255,nothing)
cv2.createTrackbar('0..255High','settings',0,255,nothing)

#TODO: Figuring out sursor position of blockade 3d

# Initialize window finder (2025 - fullscreen support)
print("=" * 50)
print("🔍 Searching for Blockade 3D Classic window...")
print("=" * 50)
if window_finder.wait_for_window(timeout=10):
    print(f"✅ Window found: '{window_finder.window_title}'")
    print(f"   Window Handle: {window_finder.window_handle}")
    
    # Get window info
    rect = window_finder.get_window_rect()
    if rect:
        left, top, right, bottom = rect
        print(f"   Window Position: ({left}, {top})")
        print(f"   Window Size: {right - left} x {bottom - top}")
    
    if window_finder.is_fullscreen():
        print("   Mode: FULLSCREEN")
        config.FULLSCREEN_MODE = True
        config.SCREEN_OFFSET_Y = 0
        # Get actual window size
        size = window_finder.get_window_size()
        if size:
            config.SCREEN_WIDTH = size[0]
            config.SCREEN_HEIGHT = size[1]
            print(f"   Screen Size: {size[0]} x {size[1]}")
    else:
        print("   Mode: WINDOWED")
        config.FULLSCREEN_MODE = False
        config.SCREEN_OFFSET_Y = 40
    
    game_region = window_finder.get_game_region()
    if game_region:
        left, top, width, height = game_region
        print(f"   Game Region: ({left}, {top}) - {width} x {height}")
    
    print("=" * 50)
    print("✅ Connected to Blockade 3D Classic!")
    print("=" * 50)
else:
    print("=" * 50)
    print("⚠️  WARNING: Game window NOT found!")
    print("   Make sure Blockade 3D Classic is running!")
    print("   Looking for windows with titles containing:")
    print("   - 'Blockade 3D Classic'")
    print("   - 'Blockade 3D'")
    print("   - 'Blockade'")
    print("   - 'Unity'")
    print("=" * 50)
    print("   Using default settings (may not work correctly)")
    print("=" * 50)

# Initialize aimbot controller
aimbot_controller = None
gui = None
gui_thread = None

# Start GUI in separate thread
try:
    from aimbot_gui import AimbotGUI
    from aimbot_controller import AimbotController
    
    def start_gui():
        global aimbot_controller, gui
        try:
            gui = AimbotGUI()
            aimbot_controller = AimbotController(gui)
            gui.aimbot_controller = aimbot_controller  # Link controller to GUI
            print("[GUI] GUI initialized successfully")
            print("[GUI] Press INSERT to show/hide the UI")
            print("[GUI] Right-click while aimbot is enabled to lock on to target")
            gui.run()
        except Exception as e:
            print(f"[GUI ERROR] GUI crashed: {e}")
            import traceback
            traceback.print_exc()
            # Try to restart GUI
            try:
                time.sleep(2)
                gui = AimbotGUI()
                aimbot_controller = AimbotController(gui)
                gui.aimbot_controller = aimbot_controller
                print("[GUI] GUI restarted after crash")
                gui.run()
            except:
                print("[GUI ERROR] Failed to restart GUI")
    
    gui_thread = threading.Thread(target=start_gui, daemon=True)
    gui_thread.start()
    print("[MAIN] GUI thread started! Press INSERT to show/hide the UI")
    print("[MAIN] Right-click while aimbot is enabled to lock on to target")
    time.sleep(2.0)  # Give GUI more time to initialize
except Exception as e:
    print(f"GUI failed to start: {e}")
    print("Running without GUI...")
    try:
        from aimbot_controller import AimbotController
        aimbot_controller = AimbotController()
    except:
        aimbot_controller = None

# for the first time
detectedX = 0
detectedY = 0

# Debug counters (initialized globally)
debug_count = 0
debug_target_count = 0

# Wallhacks: Store detected targets (module-level, no global needed)
wallhacks_targets = []

while (stopScript == False):
    st_time = time.time()
    
    # Reset wallhacks targets for this frame (module-level variable)
    wallhacks_targets.clear()  # Clear instead of reassign to avoid global issues
    
    # Ultra-Safe: Random kleine delay tussen loop iterations om patronen te voorkomen
    if random.random() < 0.1:  # 10% kans
        time.sleep(random.uniform(0.001, 0.005))  # 1-5ms extra delay
    
    # cv2.imshow('settings',img)
    # numberSettingssLow = cv2.getTrackbarPos('0..255Low','settings')
    # numberSettingsHigh = cv2.getTrackbarPos('0..255High','settings')

    # Auto-detect window position (2025 - fullscreen support)
    if config.AUTO_DETECT_WINDOW:
        game_region = window_finder.get_game_region()
        if game_region:
            left, top, width, height = game_region
            screen = grab_screen(region=(left, top, left + width, top + height), use_window_finder=True)
        else:
            # Fallback to manual region
            screen = grab_screen(region=(0, config.SCREEN_OFFSET_Y, WIDTH, HEIGTH + config.SCREEN_OFFSET_Y), use_window_finder=False)
    else:
        screen = grab_screen(region=(0, config.SCREEN_OFFSET_Y, WIDTH, HEIGTH + config.SCREEN_OFFSET_Y), use_window_finder=False)

    #masking the UI - use config values
    vertices = np.array(config.ROI_VERTICES, np.int32)

	#10 970 first
    #168 700 second


    roi_st_time = time.time()

    if(boolDisableMask == 0):
        # screen = roi(screen, [vertices])
        # screen = roi_color(screen, [vertices])
        screen = roi_fillConvexPoly(screen, vertices)
    
    # Wallhacks: Draw ESP on screen if enabled (BEFORE processing)
    # This allows ESP to be visible in the captured screen
    if wallhacks.enabled:
        # Check GUI state
        wallhacks_enabled_gui = False
        if aimbot_controller and aimbot_controller.gui:
            wallhacks_enabled_gui = aimbot_controller.gui.wallhacks_enabled
        elif gui:
            wallhacks_enabled_gui = gui.wallhacks_enabled
        
        # Only draw if enabled in GUI AND we have targets
        if wallhacks_enabled_gui and len(wallhacks_targets) > 0:
            screen = wallhacks.draw_on_screen(screen, wallhacks_targets)
            # Debug: Print wallhacks status occasionally
            if random.random() < 0.05:  # 5% chance (more frequent)
                print(f"[WALLHACKS] [OK] Drawing ESP for {len(wallhacks_targets)} targets")
        elif wallhacks_enabled_gui and len(wallhacks_targets) == 0:
            # Wallhacks enabled but no targets
            if random.random() < 0.01:  # 1% chance
                print("[WALLHACKS] [WARN] Enabled but no targets found")

    roi_ed_time = time.time()

    # print("roi:{}ms".format((roi_ed_time-roi_st_time)*1000))

    # class 'numpy.ndarray'
    # print(type(screen))
    screenGray = cv2.cvtColor(screen,  cv2.COLOR_BGR2GRAY)

    # Improved threshold for Blockade 3D Classic
    # Try adaptive threshold if simple threshold doesn't work well
    ret, whiteChannel = cv2.threshold(screenGray, config.THRESHOLD_VALUE, 255, cv2.THRESH_BINARY)
    
    # Alternative: Use adaptive threshold for varying lighting conditions
    # whiteChannel = cv2.adaptiveThreshold(screenGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
    #                                     cv2.THRESH_BINARY, 11, 2)

    notADamnThing = ""
    # iix = 0
    iix = 168
    iiy = 0
    once = 0

    # ===========================
    # Detecting a target (Ultra-Safe: Random skips to avoid patterns)
    # ===========================
    for lineX in simpleMat:
        #processing simplify matrix here
        if(once == 0):
            for rowY in lineX:
                if(iiy < WIDTH):
                    if(iix < HEIGTH):
                        if(whiteChannel[iix,iiy] == 255):
                            if(whiteChannel[iix + 1,iiy] == 255):
                                # Improved detection: Check multiple pixels to avoid muzzle flash false positives
                                # Check the pixel and surrounding area for player color
                                color_found = False
                                
                                # Check multiple nearby pixels (helps filter muzzle flash)
                                for check_offset_x in range(-1, 2):
                                    for check_offset_y in range(-1, 2):
                                        check_x = iix + 1 + check_offset_x
                                        check_y = iiy + 1 + check_offset_y
                                        
                                        # Bounds check
                                        if (0 <= check_x < HEIGTH) and (0 <= check_y < WIDTH):
                                            pixel = screen[check_x, check_y]
                                            
                                            # Check if it's a player color (not muzzle flash)
                                            if is_a_RelevantColor(pixel):
                                                color_found = True
                                                break
                                    
                                    if color_found:
                                        break
                                
                                # Only detect if we found a real player color (not muzzle flash)
                                if color_found:
                                    # bug off target shoots
                                    detectedX = str(iix)
                                    # or detectedX = str(iix+1)
                                    detectedY = str(iiy)
                                    
                                    # Detect player color for wallhacks
                                    detected_color = None
                                    for check_offset_x in range(-1, 2):
                                        for check_offset_y in range(-1, 2):
                                            check_x = iix + 1 + check_offset_x
                                            check_y = iiy + 1 + check_offset_y
                                            if (0 <= check_x < HEIGTH) and (0 <= check_y < WIDTH):
                                                pixel = screen[check_x, check_y]
                                                r, g, b = pixel[0], pixel[1], pixel[2]
                                                if r == 255 and g < config.COLOR_THRESHOLD and b < config.COLOR_THRESHOLD:
                                                    detected_color = 'red'
                                                    break
                                                elif r < config.COLOR_THRESHOLD and g == 255 and b < config.COLOR_THRESHOLD:
                                                    detected_color = 'green'
                                                    break
                                                elif r < config.COLOR_THRESHOLD and g < config.COLOR_THRESHOLD and b == 255:
                                                    detected_color = 'blue'
                                                    break
                                            if detected_color:
                                                break
                                        if detected_color:
                                            break
                                    
                                    # Store target for wallhacks
                                    if detected_color:
                                        # wallhacks_targets is already global, no need to redeclare
                                        wallhacks_targets.append((int(iix), int(iiy), detected_color))
                                    
                                    once = 1
                
                # Ultra-Safe: Soms random skip om detecteerbare patronen te voorkomen
                if random.random() < 0.05:  # 5% kans om een stap over te slaan
                    iiy += intSubdiv + random.randint(0, 2)
                else:
                    iiy += intSubdiv
                # notADamnThing = notADamnThing + str(rowY)
                # notADamnThing = notADamnThing + str(tmpScreen[iix][iiy])
            # notADamnThing = notADamnThing + '\n'
            iiy = 0
            #next line
            # Ultra-Safe: Soms variatie in increment om patronen te voorkomen
            if random.random() < 0.03:  # 3% kans op variatie
                iix += intSubdiv + random.randint(-1, 1)
            else:
                iix += intSubdiv


    #bug fix: mixed up axis
    # Ultra-Safe: Variabele deling factor (niet altijd /5) om patronen te voorkomen
    Xoffset = int(detectedY) - int(pyautogui.position()[0])
    # Variabele deling factor (4-6) om detecteerbare patronen te voorkomen
    division_factor = random.uniform(4.5, 5.5)
    Xoffset = int(Xoffset / division_factor)
    # Add small random variation to prevent pattern detection
    Xoffset += random.randint(-1, 1)

    #bug fix: mixed up axis
    Yoffset = int(detectedX) + config.SCREEN_OFFSET_Y - int(pyautogui.position()[1])
    # Variabele deling factor (4-6) om detecteerbare patronen te voorkomen
    division_factor = random.uniform(4.5, 5.5)
    Yoffset = int(Yoffset / division_factor)
    # Add small random variation to prevent pattern detection
    Yoffset += random.randint(-1, 1)

    if(once == 1):
        # EasyAntiCheat bypass: Inject random delays to avoid pattern detection
        anti_cheat.inject_delays()
        anti_cheat.simulate_human_behavior()
        anti_cheat.add_eac_safe_delay()  # EAC-specific delay
        
        # AUTO LOCK-ON: When target detected, auto-lock on nearest target if enabled
        auto_lock_enabled = True  # Default ON
        if aimbot_controller and aimbot_controller.gui:
            auto_lock_enabled = aimbot_controller.gui.auto_lock_enabled
        elif gui:
            auto_lock_enabled = gui.auto_lock_enabled
        
        if auto_lock_enabled and auto_lock.enabled and aimbot_controller and once == 1:
            # Find nearest target and lock on
            locked_target = auto_lock.auto_lock_on_shot(screen, whiteChannel)
            if locked_target:
                # Lock on to nearest target
                target_x, target_y, color = locked_target
                aimbot_controller.locked_target = (target_x, target_y)
                aimbot_controller.lock_on_active = True
                if aimbot_controller.gui:
                    aimbot_controller.gui.locked_target = locked_target
                    aimbot_controller.gui.lock_status_label.config(
                        text=f"Auto Lock-on: LOCKED (Nearest Target)", 
                        foreground="green"
                    )
                print(f"[AUTO LOCK] ✓ Locked on nearest target at ({target_y}, {target_x})")
        
        # Check if lock-on is active
        if aimbot_controller and aimbot_controller.lock_on_active:
            # Maintain lock on target
            aimbot_controller.maintain_lock()
        else:
            # Check if aimbot is enabled via GUI
            aimbot_enabled = False  # Default OFF - must enable in GUI
            soft_aim_enabled = False  # Default OFF - must enable in GUI
            
            # Get settings from GUI (check both places)
            if aimbot_controller and aimbot_controller.gui:
                aimbot_enabled = aimbot_controller.gui.aimbot_enabled
                soft_aim_enabled = aimbot_controller.gui.soft_aim_enabled
                # Also update config for soft aim
                if soft_aim_enabled:
                    config.SOFT_AIM_ENABLED = True
            elif gui:
                aimbot_enabled = gui.aimbot_enabled
                soft_aim_enabled = gui.soft_aim_enabled
                # Also update config for soft aim
                if soft_aim_enabled:
                    config.SOFT_AIM_ENABLED = True
            else:
                # No GUI - use config defaults
                try:
                    aimbot_enabled = config.AIMBOT_ENABLED if hasattr(config, 'AIMBOT_ENABLED') else False
                    soft_aim_enabled = config.SOFT_AIM_ENABLED
                except:
                    pass
            
            # DEBUG: Print status occasionally
            if random.random() < 0.02:  # 2% chance
                print(f"[MAIN LOOP] aimbot_enabled={aimbot_enabled}, soft_aim_enabled={soft_aim_enabled}, once={once}")
            
            # DEBUG: Print status (alleen eerste paar keer)
            if debug_target_count < 3:
                print(f"[DEBUG] Target detected! Xoffset: {Xoffset}, Yoffset: {Yoffset}")
                print(f"[DEBUG] Aimbot enabled: {aimbot_enabled}, Soft Aim: {soft_aim_enabled}, TAB pressed: {keyboard.is_pressed('tab')}")
                if soft_aim_enabled:
                    print("[SOFT AIM] ✓ Soft Aim is ACTIVE - Assisted aiming enabled")
                elif aimbot_enabled:
                    print("[AIMBOT] ✓ Normal Aimbot is ACTIVE - Direct aiming enabled")
                debug_target_count += 1
            
            # Check if TAB is not pressed (TAB pauzeert aimbot)
            if keyboard.is_pressed('tab') == False:
                # SOFT AIMBOT MODE (Assisted Aiming - Ultra-Safe)
                if soft_aim_enabled and not aimbot_enabled:
                    # Soft aim: Move towards target HEAD (not body center) for headshots
                    current_x, current_y = pyautogui.position()
                    target_x = current_x + Xoffset
                    target_y = current_y + Yoffset
                    
                    # Adjust target upward for headshots (soft aim goes to head)
                    try:
                        head_offset = config.SOFT_AIM_HEAD_OFFSET
                    except:
                        head_offset = -15  # Default: 15 pixels up for head
                    target_y += head_offset  # Move target up for headshot
                    
                    # Ultra-Safe: Add delay before soft aim (human reaction)
                    base_delay = random_delay(80, 150)  # Faster for headshots
                    delay = anti_detect.add_human_delay_variation(base_delay)
                    delay = anti_cheat.randomize_timing(delay)
                    time.sleep(delay)
                    
                    # Execute soft aim (now goes directly to head)
                    result = soft_aimbot.soft_aim_towards_target(target_x, target_y)
                    if result:
                        # Print occasionally to confirm it's working
                        if random.random() < 0.1:  # 10% chance (more frequent for debugging)
                            print(f"[SOFT AIM] [OK] Headshot assist active - moving towards ({target_x}, {target_y})")
                    else:
                        # Print why it failed (occasionally)
                        if random.random() < 0.05:  # 5% chance
                            print(f"[SOFT AIM] [WARN] soft_aim_towards_target returned False for ({target_x}, {target_y})")
                elif not soft_aim_enabled and not aimbot_enabled:
                    # Neither enabled - print warning occasionally
                    if random.random() < 0.01:  # 1% chance
                        print("[WARN] Aimbot and Soft Aim both OFF - enable in GUI!")
                
                # NORMAL AIMBOT MODE (Direct Aiming)
                elif aimbot_enabled:
                    # Normal aimbot behavior
                    # Add random delay before aiming (human reaction time)
                    base_delay = random_delay(80, 250)  # More realistic reaction time
                    delay = anti_detect.add_human_delay_variation(base_delay)
                    # Anti-cheat: Randomize timing further
                    delay = anti_cheat.randomize_timing(delay)
                    time.sleep(delay)
                    
                    # Normal aimbot: Direct aiming and shooting
                    # Only shoot if target is reasonably close (avoid obvious snaps)
                    distance = math.sqrt(Xoffset**2 + Yoffset**2)
                    
                    # Check if should take shot (human hesitation)
                    if distance < config.MAX_AIM_DISTANCE:
                        # Check confidence and distance
                        confidence = 1.0 - (distance / config.MAX_AIM_DISTANCE) * 0.3
                        if anti_detect.should_take_shot(distance, confidence):
                            mouse_shoot(Xoffset, Yoffset)
                        else:
                            # Hesitate - don't shoot this time
                            time.sleep(random_delay(50, 100))
                    else:
                        # For far targets, add extra delay to simulate human reaction
                        hesitation = anti_detect.simulate_human_hesitation(distance)
                        time.sleep(hesitation)
    else:
        # No target detected - add micro-movements when idle
        # DEBUG: Print als er geen target is (alleen eerste paar keer)
        if debug_count < 3:
            # Check if aimbot is enabled
            aimbot_enabled = True
            if aimbot_controller and aimbot_controller.gui:
                aimbot_enabled = aimbot_controller.gui.aimbot_enabled
            elif gui:
                aimbot_enabled = gui.aimbot_enabled
            print(f"[DEBUG] No target detected. Aimbot enabled: {aimbot_enabled}")
            debug_count += 1
        
        if random.random() < config.MICRO_MOVEMENT_CHANCE:
            anti_detect.add_micro_movements(
                pyautogui.position()[0], 
                pyautogui.position()[1], 
                config.MICRO_MOVEMENT_CHANCE
            )

        # playsound.playsound('C:/Users/jerome/Desktop/pythonBlockade3D/mp3/pew.mp3', True)

        # print("notADamnThing:\n" + notADamnThing)

        once = 0

        # print("detectedX:" + str(detectedX) +"\ndetectedY:" + str(detectedY) + "\n")
        #
        # print("pyautogui.position():"+str(pyautogui.position()))
        # print("Xoffset:"+str(Xoffset)+"\nYoffset:"+str(Yoffset))



    #cv2.imshow('windowSimpleMatrix',simpleMat)
    # cv2.imshow('windowWhite',whiteChannel)
    # cv2.imshow('screen',screen)
    # cv2.imshow('tmpScreen',tmpScreen)
    # cv2.imshow('simpleMat',simpleMat)


    # cv2.imshow('window2',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # https: // docs.opencv.org / 3.0 - beta / modules / imgproc / doc / drawing_functions.html?highlight = fillpoly  # fillconvexpoly


    #cv2.imshow('window',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
    if(keyboard.is_pressed('n')):


        stopScript = True
        cv2.destroyAllWindows()

        num_bins = 100
        # n, bins, patches = plt.hist(stats, num_bins, facecolor='blue', alpha=0.5)
        ed_total_time = time.time()
        n, bins, patches = plt.hist(stats, num_bins, facecolor='blue', alpha=0.5, label="intSubdiv:"+str(intSubdiv)+"|time(sec):"+str(ed_total_time-st_total_time)+"|"+os.path.basename(__file__))
        plt.legend()
        plt.show()

    # print("loop time :{}ms".format((time.time()-st_time)*1000))
    # FPS output removed - only show in debug mode if needed
    # Uncomment below for FPS debugging:
    # print('FPS:{}FPS'.format( (1/(time.time()-st_time))))
    stats.extend([np.uint8((1/(time.time()-st_time)))])
    # print("============================================")
# n