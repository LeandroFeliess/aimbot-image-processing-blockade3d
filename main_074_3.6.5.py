
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
    # print("tmpScreenRGBpixel:"+str(tmpScreenRGBpixel))
    # red
    # if(tmpScreenRGBpixel[1] != 0 or tmpScreenRGBpixel[2] != 0):
    #     print("there:"+str(tmpScreenRGBpixel[1])+str(tmpScreenRGBpixel[2]))
    # Use config threshold for color detection
    if((tmpScreenRGBpixel[0] == 255) and (tmpScreenRGBpixel[1] < config.COLOR_THRESHOLD) and (tmpScreenRGBpixel[2] < config.COLOR_THRESHOLD)):
        # print("tmpScreenRGBpixel:"+str(tmpScreenRGBpixel))
        return True
    if((tmpScreenRGBpixel[0] < config.COLOR_THRESHOLD) and (tmpScreenRGBpixel[1] == 255) and (tmpScreenRGBpixel[2] < config.COLOR_THRESHOLD)):
        # print("tmpScreenRGBpixel:"+str(tmpScreenRGBpixel))
        return True
    if((tmpScreenRGBpixel[0] < config.COLOR_THRESHOLD) and (tmpScreenRGBpixel[1] < config.COLOR_THRESHOLD) and (tmpScreenRGBpixel[2] == 255)):
        # print("tmpScreenRGBpixel:"+str(tmpScreenRGBpixel))
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
    # Check if should miss (human-like errors)
    if anti_detect.should_miss(config.MISS_CHANCE):
        # Miss intentionally - aim slightly off target
        miss_offset = random.uniform(15, 30)  # Miss by 15-30 pixels
        angle = random.uniform(0, 2 * math.pi)
        click_x += math.cos(angle) * miss_offset
        click_y += math.sin(angle) * miss_offset
    
    # Get current mouse position
    current_x, current_y = pyautogui.position()
    
    # Calculate target
    target_x = current_x + click_x
    target_y = current_y + click_y
    
    # Add overshoot chance
    target_x, target_y = anti_detect.add_overshoot(target_x, target_y, config.OVERSHOOT_CHANCE)
    
    # Add small imperfection to aim (configurable accuracy)
    target_x, target_y = add_aim_imperfection(
        target_x, 
        target_y, 
        accuracy=config.AIM_ACCURACY
    )
    
    # Calculate distance for speed adjustment
    distance = math.sqrt(click_x**2 + click_y**2)
    
    # Get realistic speed based on distance
    realistic_speed = anti_detect.get_realistic_aim_speed(distance, 
                                                          config.MOUSE_SPEED_MIN, 
                                                          config.MOUSE_SPEED_MAX)
    
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
    for x, y, delay in movement_points:
        rel_dx = x - current_x
        rel_dy = y - current_y
        
        # Only send movement if there's actual change
        if abs(rel_dx) > 0 or abs(rel_dy) > 0:
            keys.directMouse(dx=rel_dx, dy=rel_dy, buttons=0)
            current_x, current_y = x, y
            # Add human delay variation
            delay = anti_detect.add_human_delay_variation(delay)
            time.sleep(delay)
    
    # Add hesitation for uncertain shots
    hesitation = anti_detect.simulate_human_hesitation(distance)
    time.sleep(hesitation)
    
    # Small random delay before shooting (with variation)
    base_delay = random_delay(config.MIN_REACTION_TIME_MS, config.MAX_REACTION_TIME_MS)
    delay = anti_detect.add_human_delay_variation(base_delay)
    time.sleep(delay)
    
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
        gui = AimbotGUI()
        aimbot_controller = AimbotController(gui)
        gui.aimbot_controller = aimbot_controller  # Link controller to GUI
        gui.run()
    
    gui_thread = threading.Thread(target=start_gui, daemon=True)
    gui_thread.start()
    print("GUI started! Press INSERT to show/hide the UI")
    print("Right-click while aimbot is enabled to lock on to target")
    time.sleep(1.5)  # Give GUI time to initialize
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

while (stopScript == False):
    st_time =time.time()
    # cv2.imshow('settings',img)
    # numberSettingssLow = cv2.getTrackbarPos('0..255Low','settings')
    # numberSettingsHigh = cv2.getTrackbarPos('0..255High','settings')

    screen = grab_screen(region=(0, config.SCREEN_OFFSET_Y, WIDTH, HEIGTH + config.SCREEN_OFFSET_Y))

    #masking the UI - use config values
    vertices = np.array(config.ROI_VERTICES, np.int32)

	#10 970 first
    #168 700 second


    roi_st_time = time.time()

    if(boolDisableMask == 0):
        # screen = roi(screen, [vertices])
        # screen = roi_color(screen, [vertices])
        screen = roi_fillConvexPoly(screen, vertices)

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
    # Detecting a target
    # ===========================
    for lineX in simpleMat:
        #processing simplify matrix here
        if(once == 0):
            for rowY in lineX:
                if(iiy < WIDTH):
                    if(iix < HEIGTH):
                        if(whiteChannel[iix,iiy] == 255):
                            if(whiteChannel[iix + 1,iiy] == 255):
                                if(is_a_RelevantColor(screen[iix+1,iiy+1])):
                                # if(is_a_RelevantColor(screen[iix+intSubdiv,iiy+intSubdiv])):

                        # if(whiteChannel[iix][iiy] == 255):
                        #     if(whiteChannel[iix + 1][iiy] == 255):
                        #         if(is_a_RelevantColor(screen[iix+1][iiy+1])):
                                    # bug off target shoots
                                    detectedX = str(iix)
                                    # or detectedX = str(iix+1)
                                    detectedY = str(iiy)
                                    once = 1
                iiy += intSubdiv
                # notADamnThing = notADamnThing + str(rowY)
                # notADamnThing = notADamnThing + str(tmpScreen[iix][iiy])
            # notADamnThing = notADamnThing + '\n'
            iiy = 0
            #next line
            iix += intSubdiv


    #bug fix: mixed up axis
    Xoffset = int(detectedY) - int(pyautogui.position()[0])
    Xoffset = int(Xoffset / 5)
    # good at 10 fps w/ intSubdiv at 16
    # Xoffset = int(Xoffset / 5)

    #bug fix: mixed up axis
    Yoffset = int(detectedX) + 40 - int(pyautogui.position()[1])
    Yoffset = int(Yoffset / 5)
    # good at 10 fps w/ intSubdiv at 16
    # Yoffset = int(Yoffset / 5)

    if(once == 1):
        # Check if lock-on is active
        if aimbot_controller and aimbot_controller.lock_on_active:
            # Maintain lock on target
            aimbot_controller.maintain_lock()
        else:
            # Normal aimbot behavior
            # Add random delay before aiming (human reaction time)
            base_delay = random_delay(80, 250)  # More realistic reaction time
            delay = anti_detect.add_human_delay_variation(base_delay)
            time.sleep(delay)
            
            # Check if aimbot is enabled via GUI
            aimbot_enabled = True
            if aimbot_controller and aimbot_controller.gui:
                aimbot_enabled = aimbot_controller.gui.aimbot_enabled
            elif gui:
                aimbot_enabled = gui.aimbot_enabled
                
            # todo: add a trigger button
            if (keyboard.is_pressed('tab') == False) and aimbot_enabled:
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
    # here
    print('FPS:{}FPS'.format( (1/(time.time()-st_time))))
    # print(str(int((1/(time.time()-st_time)))))
    stats.extend([np.uint8((1/(time.time()-st_time)))])
    # print("============================================")
# n