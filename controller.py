import time
import struct
import threading

class SwitchController:
    # Standard Button Mappings
    BTN = {
        'A': 0x04, 'B': 0x02, 'X': 0x08, 'Y': 0x01,
        'L': 0x10, 'R': 0x20, 'ZL': 0x40, 'ZR': 0x80,
        'MINUS': 0x100, 'PLUS': 0x200, 'HOME': 0x1000,
        'L_R': 0x30 # Used for syncing
    }

    def __init__(self, dev="/dev/hidg0"):
        self.dev = dev
        self.lock = threading.Lock()
        self.running = False
        
        # Controller State
        self.btn_low = 0
        self.btn_high = 0
        self.lx = 128
        self.ly = 128

    def _create_report(self):
        """Generates the binary packet safely"""
        with self.lock:
            return struct.pack('<BBBBBBBB', 
                               self.btn_low, self.btn_high, 0x08, 
                               self.lx, self.ly, 128, 128, 0)

    def _force_update(self):
        """Instantly sends the state to the Switch"""
        with open(self.dev, 'rb+', buffering=0) as fd:
            fd.write(self._create_report())
            fd.flush()

    def _heartbeat(self):
        """60Hz Keep-Alive Thread"""
        with open(self.dev, 'rb+', buffering=0) as fd:
            while self.running:
                fd.write(self._create_report())
                fd.flush()
                time.sleep(0.016)

    def connect(self, sync_time=4):
        """Starts the background thread and spams L+R to sync"""
        print("Starting connection engine...")
        self.running = True
        threading.Thread(target=self._heartbeat, daemon=True).start()
        
        print("--- SYNCING ---")
        end_time = time.time() + sync_time
        while time.time() < end_time:
            self.press('L_R', hold=0.05, wait=0.05)
        print("--- CONNECTED ---")
        print("Navigating to game...")
        self.press('A', wait=0.5)       
        self.press('HOME', wait=1.0)    
        self.press('A', wait=2.0)  

    def disconnect(self):
        """Stops the background thread"""
        self.running = False
        print("Disconnected.")

    def press(self, button_name, hold=0.15, wait=0.15):
        """Presses a button by name (e.g., 'A', 'HOME')"""
        val = self.BTN.get(button_name.upper())
        if not val:
            print(f"Error: Unknown button '{button_name}'")
            return

        print(f" -> Pressing {button_name}")
        with self.lock:
            if val <= 0xFF: self.btn_low = val
            else: self.btn_high = (val >> 8)
        self._force_update()
        
        time.sleep(hold)
        
        with self.lock:
            self.btn_low = 0
            self.btn_high = 0
        self._force_update()
        
        time.sleep(wait)

    def move_stick(self, x, y, duration, wait=0.15):
        """Moves the left stick to X/Y coordinates"""
        print(f" -> Moving Stick (X:{x}, Y:{y}) for {duration}s")
        with self.lock:
            self.lx = x
            self.ly = y
        self._force_update()
        
        time.sleep(duration)
        
        with self.lock:
            self.lx = 128
            self.ly = 128
        self._force_update()
        
        time.sleep(wait)

    def release_all(self):
        """Emergency stop: releases all buttons and centers sticks instantly"""
        with self.lock:
            self.btn_low = 0
            self.btn_high = 0
            self.lx = 128
            self.ly = 128
        self._force_update()