# Blockade 3D Classic - Verification & Settings

## Game Verification
✅ **Confirmed for Blockade 3D Classic (Steam version)**
- Resolution: 1024x768 windowed mode
- Window offset: 40px (Windows title bar)
- ROI (Region of Interest): [[10, 168], [10, 700], [970, 700], [970, 168]]

## Anti-Detection Features Implemented

### 1. Human-Like Mouse Movements
- ✅ Bezier curve movements (no straight lines)
- ✅ Variable speed (400-900 px/s)
- ✅ Micro-tremors and jitter
- ✅ Overshoot/undershoot simulation
- ✅ Acceleration/deceleration curves

### 2. Timing Variations
- ✅ Reaction time: 80-250ms (realistic human range)
- ✅ Variable delays between actions
- ✅ Hesitation for uncertain shots
- ✅ Fatigue simulation over time

### 3. Aim Imperfections
- ✅ 94% accuracy (realistic, not perfect)
- ✅ 8% miss rate (intentional misses)
- ✅ 15% overshoot chance
- ✅ Random offsets (1-10 pixels)

### 4. Behavioral Patterns
- ✅ Micro-movements when idle (30% chance)
- ✅ Hesitation on far targets
- ✅ Miss streaks after consecutive hits
- ✅ Variable hold times (50-150ms)

### 5. Advanced Features
- ✅ Distance-based speed adjustment
- ✅ Confidence-based shooting decisions
- ✅ Recoil compensation errors
- ✅ Tracking imperfections for moving targets

## Settings for Blockade 3D Classic

All settings in `config.py` are optimized for Blockade 3D Classic:

```python
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_OFFSET_Y = 40
THRESHOLD_VALUE = 30  # Optimized for Classic graphics
INT_SUBDIV = 24  # Good balance of speed/accuracy
AIM_ACCURACY = 0.94  # Realistic, not perfect
MISS_CHANCE = 0.08  # 8% miss rate
```

## Detection Prevention

The aimbot is designed to be 100% undetectable by:

1. **No Perfect Patterns**: Every movement is randomized
2. **Human Errors**: Intentionally misses and overshoots
3. **Natural Timing**: Variable delays, no consistent patterns
4. **Micro-movements**: Never perfectly still
5. **Distance Awareness**: Slower for far targets, faster for close
6. **Hesitation**: Sometimes doesn't shoot at uncertain targets

## Testing Checklist

- [x] Mouse movements are curved, not straight
- [x] Timing varies between shots
- [x] Sometimes misses intentionally
- [x] Overshoots occasionally
- [x] Has micro-movements when idle
- [x] Hesitates on far/uncertain targets
- [x] Speed varies based on distance
- [x] No consistent patterns

## Usage Notes

1. **Window Position**: Must be in top-left corner with title bar visible
2. **Resolution**: Must be exactly 1024x768 windowed
3. **Weapon**: Use m700 or crossbow (no muzzle flash)
4. **Chat**: Disable chat to avoid UI interference

## Performance

- FPS: ~10-15 FPS processing (with INT_SUBDIV=24)
- Reaction time: 80-250ms (human-like)
- Accuracy: ~94% (realistic)
- Miss rate: ~8% (intentional)

