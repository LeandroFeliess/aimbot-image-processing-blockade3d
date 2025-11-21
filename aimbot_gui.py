"""
Aimbot GUI Controller
Modern UI for Blockade 3D Classic aimbot with right-click lock-on feature
"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import keyboard
import pyautogui
from pynput import mouse
import config


class AimbotGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Blockade 3D Classic Aimbot")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        # State variables
        self.aimbot_enabled = False
        self.lock_on_enabled = False
        self.ui_visible = True
        self.locked_target = None
        self.lock_thread = None
        self.aimbot_thread = None
        self.aimbot_controller = None  # Will be set by main script
        
        # Mouse listener for right-click detection
        self.mouse_listener = None
        
        # Setup UI
        self.setup_ui()
        
        # Setup keyboard hooks
        self.setup_keyboard_hooks()
        
        # Setup mouse listener
        self.setup_mouse_listener()
        
        # Make window always on top
        self.root.attributes('-topmost', True)
        
    def setup_ui(self):
        """Create the GUI interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Blockade 3D Classic Aimbot", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Status section
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Aimbot: OFF", 
                                      foreground="red", font=("Arial", 12))
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        self.lock_status_label = ttk.Label(status_frame, text="Lock-on: OFF", 
                                          foreground="red", font=("Arial", 12))
        self.lock_status_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        # Controls section
        controls_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        controls_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Aimbot toggle
        self.aimbot_button = ttk.Button(controls_frame, text="Enable Aimbot", 
                                        command=self.toggle_aimbot, width=20)
        self.aimbot_button.grid(row=0, column=0, pady=5)
        
        # Lock-on toggle
        self.lock_button = ttk.Button(controls_frame, text="Enable Lock-on", 
                                      command=self.toggle_lock_on, width=20)
        self.lock_button.grid(row=1, column=0, pady=5)
        
        # Settings section
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="10")
        settings_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Aim accuracy
        ttk.Label(settings_frame, text="Aim Accuracy:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.accuracy_var = tk.DoubleVar(value=config.AIM_ACCURACY)
        accuracy_scale = ttk.Scale(settings_frame, from_=0.85, to=0.99, 
                                   variable=self.accuracy_var, orient=tk.HORIZONTAL, length=200)
        accuracy_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        self.accuracy_label = ttk.Label(settings_frame, text=f"{config.AIM_ACCURACY:.2f}")
        self.accuracy_label.grid(row=0, column=2, padx=5)
        accuracy_scale.configure(command=self.update_accuracy_label)
        
        # Reaction time
        ttk.Label(settings_frame, text="Reaction Time (ms):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.reaction_min_var = tk.IntVar(value=config.MIN_REACTION_TIME_MS)
        self.reaction_max_var = tk.IntVar(value=config.MAX_REACTION_TIME_MS)
        reaction_frame = ttk.Frame(settings_frame)
        reaction_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E))
        ttk.Spinbox(reaction_frame, from_=10, to=500, width=8, 
                   textvariable=self.reaction_min_var).grid(row=0, column=0, padx=2)
        ttk.Label(reaction_frame, text=" - ").grid(row=0, column=1)
        ttk.Spinbox(reaction_frame, from_=10, to=500, width=8, 
                   textvariable=self.reaction_max_var).grid(row=0, column=2, padx=2)
        
        # Max aim distance
        ttk.Label(settings_frame, text="Max Aim Distance:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.distance_var = tk.IntVar(value=config.MAX_AIM_DISTANCE)
        distance_spin = ttk.Spinbox(settings_frame, from_=100, to=1000, width=10, 
                                   textvariable=self.distance_var)
        distance_spin.grid(row=2, column=1, sticky=tk.W, padx=5)
        
        # Info section
        info_frame = ttk.LabelFrame(main_frame, text="Hotkeys", padding="10")
        info_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        info_text = """INSERT - Show/Hide UI
RIGHT CLICK - Lock on target
TAB - Pause aimbot (in game)
N - Stop script"""
        
        ttk.Label(info_frame, text=info_text, justify=tk.LEFT).grid(row=0, column=0, sticky=tk.W)
        
        # Apply button
        apply_button = ttk.Button(main_frame, text="Apply Settings", 
                                 command=self.apply_settings, width=20)
        apply_button.grid(row=5, column=0, columnspan=2, pady=10)
        
    def update_accuracy_label(self, value=None):
        """Update accuracy label when scale changes"""
        self.accuracy_label.config(text=f"{self.accuracy_var.get():.2f}")
        
    def toggle_aimbot(self):
        """Toggle aimbot on/off"""
        self.aimbot_enabled = not self.aimbot_enabled
        if self.aimbot_enabled:
            self.aimbot_button.config(text="Disable Aimbot")
            self.status_label.config(text="Aimbot: ON", foreground="green")
            # Start aimbot thread
            if self.aimbot_thread is None or not self.aimbot_thread.is_alive():
                self.aimbot_thread = threading.Thread(target=self.aimbot_loop, daemon=True)
                self.aimbot_thread.start()
        else:
            self.aimbot_button.config(text="Enable Aimbot")
            self.status_label.config(text="Aimbot: OFF", foreground="red")
            
    def toggle_lock_on(self):
        """Toggle lock-on feature"""
        self.lock_on_enabled = not self.lock_on_enabled
        if self.lock_on_enabled:
            self.lock_button.config(text="Disable Lock-on")
            self.lock_status_label.config(text="Lock-on: ON (Right-click to lock)", 
                                          foreground="green")
        else:
            self.lock_button.config(text="Enable Lock-on")
            self.lock_status_label.config(text="Lock-on: OFF", foreground="red")
            self.locked_target = None
            # Disable lock in controller
            if self.aimbot_controller:
                self.aimbot_controller.lock_on_active = False
                self.aimbot_controller.locked_target = None
            
    def apply_settings(self):
        """Apply settings from UI to config"""
        config.AIM_ACCURACY = self.accuracy_var.get()
        config.MIN_REACTION_TIME_MS = self.reaction_min_var.get()
        config.MAX_REACTION_TIME_MS = self.reaction_max_var.get()
        config.MAX_AIM_DISTANCE = self.distance_var.get()
        messagebox.showinfo("Settings", "Settings applied successfully!")
        
    def setup_keyboard_hooks(self):
        """Setup keyboard hooks for Insert key"""
        def on_insert_press():
            self.toggle_ui_visibility()
            
        keyboard.on_press_key('insert', lambda _: on_insert_press())
        
    def toggle_ui_visibility(self):
        """Show/hide UI window"""
        self.ui_visible = not self.ui_visible
        if self.ui_visible:
            self.root.deiconify()
            self.root.attributes('-topmost', True)
        else:
            self.root.withdraw()
            
    def setup_mouse_listener(self):
        """Setup mouse listener for right-click detection"""
        def on_click(x, y, button, pressed):
            if button == mouse.Button.right and pressed:
                if self.lock_on_enabled and self.aimbot_enabled:
                    # Lock on to target at mouse position using controller
                    if self.aimbot_controller:
                        target = self.aimbot_controller.lock_on_to_position(x, y)
                        if target:
                            self.locked_target = target
                            self.lock_status_label.config(
                                text=f"Lock-on: LOCKED at ({target[1]}, {target[0]})", 
                                foreground="green"
                            )
                    else:
                        # Fallback if controller not available
                        self.lock_on_target(x, y)
                    
        self.mouse_listener = mouse.Listener(on_click=on_click)
        self.mouse_listener.start()
        
    def lock_on_target(self, x, y):
        """Lock on to target at screen coordinates (fallback method)"""
        screen_x = x
        screen_y = y
        
        # Convert screen coordinates to game coordinates
        game_x = screen_x
        game_y = screen_y - config.SCREEN_OFFSET_Y
        
        if 0 <= game_x < config.SCREEN_WIDTH and 0 <= game_y < config.SCREEN_HEIGHT:
            self.locked_target = (game_y, game_x)
            self.lock_status_label.config(text=f"Lock-on: LOCKED at ({game_x}, {game_y})", 
                                         foreground="green")
                
    def lock_on_loop(self):
        """Main loop for lock-on tracking (now handled by controller)"""
        # This is now handled by the aimbot_controller
        pass
            
    def aimbot_loop(self):
        """Main aimbot loop - this will integrate with the existing aimbot code"""
        # This is a placeholder - the actual aimbot logic is in main_074_3.6.5.py
        # This will be called from the main script
        pass
        
    def run(self):
        """Start the GUI"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.cleanup()
            
    def cleanup(self):
        """Cleanup resources"""
        if self.mouse_listener:
            self.mouse_listener.stop()
        self.root.quit()


if __name__ == "__main__":
    app = AimbotGUI()
    app.run()

