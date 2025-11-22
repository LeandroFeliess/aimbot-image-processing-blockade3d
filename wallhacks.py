"""
Wallhacks/ESP - Draw outlines around detected targets
Ultra-Safe: Uses external overlay, no game memory access
"""
import cv2
import numpy as np
import threading
import time
import random
import config


class Wallhacks:
    """
    Wallhacks/ESP system - Draws outlines around detected targets
    Ultra-Safe: External overlay, no memory injection
    """
    
    def __init__(self):
        self.enabled = False
        self.overlay_window = None
        self.targets = []  # List of detected targets [(x, y, color), ...]
        self.overlay_thread = None
        self.running = False
        
    def enable(self):
        """Enable wallhacks/ESP"""
        if not self.enabled:
            self.enabled = True
            self.running = True
            self.overlay_thread = threading.Thread(target=self._overlay_loop, daemon=True)
            self.overlay_thread.start()
            print("[WALLHACKS] [OK] Wallhacks ENABLED - ESP overlay active")
    
    def disable(self):
        """Disable wallhacks/ESP"""
        if self.enabled:
            self.enabled = False
            self.running = False
            if self.overlay_window is not None:
                try:
                    cv2.destroyWindow("ESP Overlay")
                except:
                    pass
            print("[WALLHACKS] [OFF] Wallhacks DISABLED")
    
    def update_targets(self, targets):
        """
        Update detected targets for ESP drawing
        targets: List of (x, y, color) tuples
        color: 'red', 'green', or 'blue'
        """
        self.targets = targets
    
    def _overlay_loop(self):
        """Main overlay loop - draws ESP on separate window"""
        try:
            # Create overlay window (borderless, always on top)
            overlay = np.zeros((config.SCREEN_HEIGHT, config.SCREEN_WIDTH, 3), dtype=np.uint8)
            
            while self.running and self.enabled:
                # Clear overlay
                overlay.fill(0)
                
                # Draw ESP for each target
                for target in self.targets:
                    if len(target) >= 3:
                        x, y, color = target[0], target[1], target[2]
                        
                        # Convert color name to BGR
                        if color == 'red':
                            bgr_color = (0, 0, 255)  # Red in BGR
                        elif color == 'green':
                            bgr_color = (0, 255, 0)  # Green in BGR
                        elif color == 'blue':
                            bgr_color = (255, 0, 0)  # Blue in BGR
                        else:
                            bgr_color = (255, 255, 255)  # White default
                        
                        # Draw box around target (ESP)
                        box_size = 30
                        thickness = 2
                        
                        # Top-left corner
                        pt1 = (max(0, int(y - box_size//2)), max(0, int(x - box_size//2)))
                        # Bottom-right corner
                        pt2 = (min(config.SCREEN_WIDTH, int(y + box_size//2)), 
                               min(config.SCREEN_HEIGHT, int(x + box_size//2)))
                        
                        # Draw rectangle (ESP box)
                        cv2.rectangle(overlay, pt1, pt2, bgr_color, thickness)
                        
                        # Draw crosshair at target center
                        crosshair_size = 5
                        cv2.line(overlay, 
                                (int(y), int(x - crosshair_size)), 
                                (int(y), int(x + crosshair_size)), 
                                bgr_color, 1)
                        cv2.line(overlay, 
                                (int(y - crosshair_size), int(x)), 
                                (int(y + crosshair_size), int(x)), 
                                bgr_color, 1)
                
                # Show overlay (transparent background, only lines visible)
                # Note: This creates a separate window - for true overlay, would need DirectX/OpenGL
                # For now, we'll use a simpler approach with screen annotation
                
                time.sleep(0.033)  # ~30 FPS update rate
                
        except Exception as e:
            print(f"[WALLHACKS ERROR] {e}")
            import traceback
            traceback.print_exc()
    
    def draw_on_screen(self, screen, targets):
        """
        Draw ESP directly on screen capture (for overlay effect)
        Returns modified screen with ESP drawn
        NOTE: This draws on the captured screen, but you won't see it unless you use cv2.imshow
        For true overlay, we need a separate overlay window (see _overlay_loop)
        """
        if not self.enabled:
            return screen
        
        if not targets or len(targets) == 0:
            return screen
        
        screen_copy = screen.copy()
        
        # Draw ESP for each target
        for target in targets:
            if len(target) >= 3:
                x, y, color = target[0], target[1], target[2]
                
                # Convert color name to BGR
                if color == 'red':
                    bgr_color = (0, 0, 255)  # Red
                elif color == 'green':
                    bgr_color = (0, 255, 0)  # Green
                elif color == 'blue':
                    bgr_color = (255, 0, 0)  # Blue
                else:
                    bgr_color = (255, 255, 255)  # White
                
                # Draw box around target (larger for visibility)
                box_size = 40
                thickness = 3
                
                # Bounds check
                if not (0 <= x < screen.shape[0] and 0 <= y < screen.shape[1]):
                    continue
                
                # Top-left
                pt1 = (max(0, int(y - box_size//2)), max(0, int(x - box_size//2)))
                # Bottom-right
                pt2 = (min(screen.shape[1], int(y + box_size//2)), 
                       min(screen.shape[0], int(x + box_size//2)))
                
                # Draw rectangle
                cv2.rectangle(screen_copy, pt1, pt2, bgr_color, thickness)
                
                # Draw crosshair at target center
                crosshair_size = 6
                cv2.line(screen_copy, 
                        (int(y), max(0, int(x - crosshair_size))), 
                        (int(y), min(screen.shape[0], int(x + crosshair_size))), 
                        bgr_color, 2)
                cv2.line(screen_copy, 
                        (max(0, int(y - crosshair_size)), int(x)), 
                        (min(screen.shape[1], int(y + crosshair_size)), int(x)), 
                        bgr_color, 2)
        
        # Show wallhacks overlay window (always visible)
        # This creates a separate window that shows the ESP overlay
        try:
            # Resize for display (smaller window)
            display_size = (640, 360)  # 16:9 aspect ratio
            display = cv2.resize(screen_copy, display_size)
            cv2.imshow('Wallhacks ESP', display)
            cv2.waitKey(1)  # Non-blocking - allows other code to run
        except Exception as e:
            # If window was closed, recreate it
            pass
        
        return screen_copy


# Global instance
wallhacks = Wallhacks()

