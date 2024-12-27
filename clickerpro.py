import tkinter as tk
from tkinter import messagebox
import pyautogui
import random
import threading
import time
import keyboard
import mouse  # Ensure you have the mouse library installed

class ClickerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Clicker App")
        
        self.locations = []
        self.running = False
        
        self.interval_label = tk.Label(master, text="Intervals (comma-separated, in seconds):")
        self.interval_label.pack()
        self.interval_entry = tk.Entry(master)
        self.interval_entry.pack()
        
        self.stop_interval_label = tk.Label(master, text="Stop Intervals (comma-separated, in seconds):")
        self.stop_interval_label.pack()
        self.stop_interval_entry = tk.Entry(master)
        self.stop_interval_entry.pack()
        
        self.click_type_label = tk.Label(master, text="Click Type:")
        self.click_type_label.pack()
        self.click_type_var = tk.StringVar(value="single")
        self.single_click_radio = tk.Radiobutton(master, text="Single Click", variable=self.click_type_var, value="single")
        self.single_click_radio.pack()
        self.double_click_radio = tk.Radiobutton(master, text="Double Click", variable=self.click_type_var, value="double")
        self.double_click_radio.pack()
        
        self.start_button = tk.Button(master, text="Start", command=self.start_clicking)
        self.start_button.pack()
        self.stop_button = tk.Button(master, text="Stop", command=self.stop_clicking)
        self.stop_button.pack()
        
        self.add_location_button = tk.Button(master, text="Add Click Location", command=self.add_location)
        self.add_location_button.pack()
        
        # Label for instructions
        self.instruction_label = tk.Label(master, text="", fg="blue")
        self.instruction_label.pack()
        
        # Label for location count
        self.location_count_label = tk.Label(master, text="Locations Captured: 0", fg="green")
        self.location_count_label.pack()

        # Bind keyboard shortcuts
        keyboard.add_hotkey('F9', self.start_clicking)
        keyboard.add_hotkey('F10', self.stop_clicking)

    def add_location(self):
        # Set instruction text
        self.instruction_label.config(text="Click anywhere on the screen to add the location.")
        # Start listening for the next mouse click
        mouse.hook(self.capture_location)

    def capture_location(self, event):
        # Check if the event is a mouse button press
        if event.event_type == 'down' and event.button == 'left':  # Check for left mouse button press
            x, y = pyautogui.position()  # Get the current mouse position
            self.locations.append((x, y))
            self.instruction_label.config(text=f"Location ({x}, {y}) added. Click again to add more.")
            self.update_location_count()  # Update the count display
            mouse.unhook(self.capture_location)  # Stop listening after capturing the location

    def update_location_count(self):
        # Update the label to show the count of captured locations
        count = len(self.locations)
        self.location_count_label.config(text=f"Locations Captured: {count}")

    def start_clicking(self, event=None):
        if not self.running:
            self.running = True
            self.clicker_thread = threading.Thread(target=self.clicker)
            self.clicker_thread.start()
        
    def stop_clicking(self, event=None):
        self.running = False
        if hasattr(self, 'clicker_thread'):
            self.clicker_thread.join()
        
    def clicker(self):
        while self.running:
            if not self.locations:
                continue
            
            interval_input = self.interval_entry.get()
            intervals = [float(i) for i in interval_input.split(',') if i.strip()]
            stop_interval_input = self.stop_interval_entry.get()
            stop_intervals = [float(i) for i in stop_interval_input.split(',') if i.strip()]
            click_type = self.click_type_var.get()
            
            x, y = random.choice(self.locations)
            pyautogui.moveTo(x, y)
            
            if click_type == "single":
                pyautogui.click()
            else:
                pyautogui.doubleClick()
            
            time.sleep(random.choice(intervals))
            
            if random.random() < 0.1:  # 10% chance to stop clicking
                time.sleep(random.choice(stop_intervals))
                
if __name__ == "__main__":
    root = tk.Tk()
    app = ClickerApp(root)
    root.mainloop()
