import numpy as np
import cv2
import time
import random
from grabscreen import grab_screen
from keys import Keys

# Removed playsound import (not used)

HEIGTH = 768
WIDTH = 1024

keys = Keys()


def move_mouse(click_x, click_y):
    """Move mouse with human-like behavior"""
    # Small random delay before action
    time.sleep(random.uniform(0.05, 0.15))
    keys.keys_worker.sendMouse(dx=0, dy=0, buttons=keys.mouse_lb_press)
    time.sleep(random.uniform(0.8, 1.2))  # Variable hold time
    keys.keys_worker.sendMouse(dx=-1, dy=0, buttons=keys.mouse_lb_release)

for i in list(range(4))[::-1]:
    print(i+1)
    time.sleep(1)

last_time = time.time()

DEBUG = 0
DEBUGwhiteGray = 1

toolDEBUG = 0

boolMoveMouse = 0
boolMoveSlowMouse = 0
boolMoveMouseShoot = 1

boolSlowFPS = 0

boolMat = 0
##24 ok
#18 ok pebkac and drunk
intSubdiv = 18
#bugfix missing last lines
iHEIGTH = (HEIGTH//intSubdiv)
iWIDTH = (WIDTH//intSubdiv)
#bugfix inverted width height
simpleMat = np.zeros((iHEIGTH,iWIDTH,1), np.uint8)

boolDisableMask = 0

img = np.zeros((50,400,3), np.uint8)

#TODO: Figuring out sursor position of blockade 3d

iCoin = 0


while (iCoin<50):
#while (True):

    screen = grab_screen(region=(0,0,WIDTH,HEIGTH))

    screenGray = cv2.cvtColor(screen,  cv2.COLOR_BGR2GRAY)

    # Adaptive threshold for better detection in Blockade 3D Classic
    # Try multiple threshold values for better window border detection
    ret,whiteChannel = cv2.threshold(screenGray, 30, 255, cv2.THRESH_BINARY)
    
    # Alternative: Use adaptive threshold if simple threshold fails
    # whiteChannel = cv2.adaptiveThreshold(screenGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
    #                                     cv2.THRESH_BINARY, 11, 2)

    notADamnThing = ""
    iix = 0
    iiy = 0
    detectedX = 0
    detectedY = 0
    once = 0
    # Improved detection: look for window border in top-left area
    # Check first few rows and columns for white pixels (window border)
    transWhiteChannel = whiteChannel.transpose()
    
    # Search in a slightly larger area for better detection
    search_width = min(50, WIDTH)
    search_height = min(10, HEIGTH)
    
    for lineX in simpleMat:
        #processing simplify matrix here
        for rowY in lineX:
            if(iiy < search_width):
                if(iix < search_height):
                    # Check for white pixel (window border)
                    if(transWhiteChannel[iiy][iix] == 255):
                        # Verify it's not just noise - check surrounding pixels
                        if(iix > 0 and iiy > 0):
                            # Check if we have a consistent border pattern
                            border_count = 0
                            for dx in [-1, 0, 1]:
                                for dy in [-1, 0, 1]:
                                    if 0 <= iiy+dy < WIDTH and 0 <= iix+dx < HEIGTH:
                                        if transWhiteChannel[iiy+dy][iix+dx] == 255:
                                            border_count += 1
                            
                            # If we have enough border pixels, it's likely the window edge
                            if border_count >= 3 and once == 0:
                                once = 1
                                detectedX = str(iix)
                                detectedY = str(iiy)
                                print(f"Window corner detected at: ({iix}, {iiy})")
                                break
            iiy += 1
        if once:
            break
        #next line
        iix += 1

    if(once):
        move_mouse(int(detectedX),int(detectedY))


    #TODO:adding mouse pointing point here

    #print('{} FPS'.format( 1/(time.time()-last_time)))
    #print('{} msec'.format( (time.time()-last_time)*1000))
    print('{} FPS'.format( (1/(time.time()-last_time))))
    last_time = time.time()

    #cv2.imshow('windowSimpleMatrix',simpleMat)

    #cv2.imshow('windowWhite',whiteChannel)

    #my code here

    #cv2.imshow('window',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
    #if cv2.waitKey(25) & 0xFF == ord('q'):
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

    iCoin += 1

