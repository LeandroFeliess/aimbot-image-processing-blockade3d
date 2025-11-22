# aimbot-image-processing-blockade3d (Updated for Blockade 3D Classic - 2025)

> **⚡ Snel starten? Zie: [SNEL_START_GUIDE.md](SNEL_START_GUIDE.md)**

## What is it:

A script to aimbot at anyone and shoot anyone in Blockade 3D Classic.

It is a script to process on the rendered image of the game while it is in window mode 1024*768,
it will shoot at anything that looks remotely like a head.

**Updated 2024**: Code has been modernized and improved with undetectable human-like mouse movements,
bezier curves, random delays, and aim imperfections to avoid detection.

## Why:

I learnt a little bit of python through this project. And wanted to explore what is possible with
static rules coding when it comes to image processing. Another project might follow using a
Machine Learning technology.

## What does it look like:

Actually it is more difficult to play with it than without it.

Don't hesitate to take a peek at each video as I was progressing in the development.

https://www.youtube.com/watch?v=0JrUKxCvSsE&list=PL4ftK5Ce2m_ZT_fHOl6UeiZ9gOrT6PlHu

My first attempt was (hilarious):

https://www.youtube.com/watch?v=PNkFDKUuN-g

## Installation:

**📖 Voor een uitgebreide stap-voor-stap handleiding, zie: [INSTALLATIE_GUIDE.md](INSTALLATIE_GUIDE.md)**

### Quick Start:

1. Install Python 3.8 or higher (tested on Python 3.10+)
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to use it:

**📖 Zie [INSTALLATIE_GUIDE.md](INSTALLATIE_GUIDE.md) voor een complete stap-voor-stap handleiding!**

### Quick Steps (2025 - Fullscreen Support!):

1. **Setup Game**: Start Blockade 3D Classic (windowed OR fullscreen - both work!)

2. **Start Aimbot** (no calibration needed!):
   ```bash
   python main_074_3.6.5.py
   ```
   The aimbot automatically finds the game window!

3. **Open GUI**: Press **INSERT** key

4. **Enable**: Click "Enable Aimbot" in GUI

5. **Play**: Join game, equip m700/crossbow, disable chat (ESC)

**✅ NEW (2025)**: 
- ✅ Fullscreen support
- ✅ Auto window detection
- ✅ No manual calibration needed
- ✅ Anti-cheat bypass features

### GUI Controls:
   - **INSERT** - Show/hide UI
   - **Right-click** - Lock on target (when lock-on enabled)
   - **TAB** - Pause aimbot (in-game)
   - **N** - Stop script

### For detailed instructions, see [INSTALLATIE_GUIDE.md](INSTALLATIE_GUIDE.md)

## Tips:

- **INSERT key** will show/hide the GUI (press in-game)

- **Right-click** while aimbot is enabled to lock on to a target's head (the aimbot will track that target)

- **N key** will stop the script gracefully and show performance statistics

- **TAB key** will show you the scoreboard in game and lets you use your mouse (aimbot pauses)

- Don't make it run for too long if you don't have much memory:
  the script will collect statistics about how fast the script is running and
  show you the results at the end (everything is local, nothing on the internet)

- Adjust settings in `config.py` to fine-tune:
  - `INT_SUBDIV`: Processing speed (18-24 recommended, higher = faster but less accurate)
  - `AIM_ACCURACY`: Aim precision (0.95-0.98 recommended for human-like behavior)
  - `THRESHOLD_VALUE`: Detection sensitivity (20-40, adjust if targets aren't detected)
  - Mouse speed and reaction times for more/less human-like behavior

## New Features (2024 Update):

- **Human-like mouse movements**: Uses bezier curves for natural movement patterns
- **Aim imperfections**: Adds small random offsets to simulate human error
- **Variable timing**: Random delays and reaction times for undetectable behavior
- **Configurable settings**: Easy to adjust via `config.py`
- **Modern code**: Fixed deprecated functions, improved error handling
- **Better detection**: Improved threshold and border detection for Blockade 3D Classic


## How to work on it:

**Updated**: Now works with Python 3.8+ (tested on Python 3.10+)

Install dependencies:
```bash
pip install -r requirements.txt
```

Required modules:
- numpy
- opencv-python (cv2)
- pyautogui
- keyboard
- matplotlib
- pywin32

I have Blockade 3D Classic installed on Steam. You will have an easier time if you have a profile with the
m700 or the crossbow.

Please read ideas inside the TODO.md

## Undetectable Features:

The updated code includes several features to make the aimbot less detectable:

1. **Bezier curve movements**: Mouse moves in natural curved paths, not straight lines
2. **Variable speed**: Movement speed varies randomly (500-800 pixels/second)
3. **Aim imperfections**: 95-98% accuracy with small random offsets
4. **Reaction delays**: Random delays before aiming (50-200ms)
5. **Distance limits**: Won't aim at targets too far away (prevents obvious snaps)
6. **Variable hold times**: Mouse button hold time varies (50-150ms)

Adjust these in `config.py` to fine-tune the behavior.


## Credits:

Thanks to Daniel (for the keys.py library and the constructive criticism): 

https://github.com/daniel-kukiela

https://twitter.com/daniel_kukiela


And for Sentdex (for little bit of code (Region Of interest) and for inspiring me in the first place):

https://github.com/Sentdex

https://www.youtube.com/user/sentdex
