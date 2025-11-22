"""
Find Blockade 3D Classic Installation
Zoekt waar Blockade 3D Classic geinstalleerd is
"""
import os
import win32api
import win32con

print("=" * 60)
print("BLOCKADE 3D CLASSIC INSTALLATION FINDER")
print("=" * 60)
print()

# Common installation locations
search_paths = [
    r"C:\Program Files (x86)\BLOCKADE",
    r"C:\Program Files\BLOCKADE",
    r"C:\Program Files (x86)\Steam\steamapps\common",
    r"C:\Program Files\Steam\steamapps\common",
    os.path.expanduser(r"~\AppData\Local\Programs"),
    os.path.expanduser(r"~\Desktop"),
    r"C:\Games",
    r"D:\Games",
    r"E:\Games",
]

print("[INFO] Searching for Blockade 3D Classic installation...")
print()

found = False

for base_path in search_paths:
    if not os.path.exists(base_path):
        continue
    
    print(f"[INFO] Checking: {base_path}")
    
    # Search for blockade folders
    try:
        for root, dirs, files in os.walk(base_path):
            # Limit depth to avoid too much searching
            depth = root[len(base_path):].count(os.sep)
            if depth > 3:
                dirs[:] = []  # Don't recurse deeper
                continue
            
            for dir_name in dirs:
                if "blockade" in dir_name.lower():
                    full_path = os.path.join(root, dir_name)
                    print(f"  [FOUND] {full_path}")
                    
                    # List contents
                    try:
                        contents = os.listdir(full_path)
                        print(f"    Contents: {len(contents)} items")
                        for item in contents[:10]:  # Show first 10
                            item_path = os.path.join(full_path, item)
                            if os.path.isfile(item_path):
                                size = os.path.getsize(item_path)
                                print(f"      File: {item} ({size} bytes)")
                            else:
                                print(f"      Dir:  {item}")
                        if len(contents) > 10:
                            print(f"      ... and {len(contents) - 10} more items")
                    except Exception as e:
                        print(f"    [ERROR] Could not list contents: {e}")
                    
                    found = True
                    print()
    except Exception as e:
        pass

# Also check running processes
print("[INFO] Checking running processes...")
try:
    import psutil
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            if 'blockade' in proc.info['name'].lower():
                print(f"  [FOUND] Process: {proc.info['name']}")
                if proc.info['exe']:
                    exe_dir = os.path.dirname(proc.info['exe'])
                    print(f"    Location: {exe_dir}")
                    found = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
except ImportError:
    print("  [WARN] psutil not installed - cannot check processes")
except Exception as e:
    print(f"  [ERROR] {e}")

print()
print("=" * 60)
if found:
    print("[OK] Blockade installation found!")
else:
    print("[FAIL] Blockade installation NOT found in common locations")
    print("   Please provide the installation path manually")
print("=" * 60)

