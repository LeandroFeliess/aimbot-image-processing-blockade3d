"""
Fix all test scripts - remove emojis for Windows compatibility
"""
import os
import re

files = [
    "test_window_detection.py",
    "test_screen_capture.py",
    "test_target_detection.py",
    "test_wallhacks.py",
    "test_gui.py"
]

emoji_map = {
    "✅": "[OK]",
    "❌": "[FAIL]",
    "🔍": "[INFO]",
    "📸": "[CAPTURE]",
    "🎨": "[DRAW]",
    "🖥️": "[GUI]",
    "⚠️": "[WARN]",
    "🧪": "[TEST]",
    "📊": "[STATS]",
    "🎉": "[SUCCESS]"
}

for file in files:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        for emoji, replacement in emoji_map.items():
            content = content.replace(emoji, replacement)
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed: {file}")

print("All files fixed!")

