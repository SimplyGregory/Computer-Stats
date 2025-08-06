import tkinter as tk
import psutil 
import threading
import time
import os
from pynput.mouse import Button,Controller
import keyboard
import subprocess
options = ["Option:Auto Clicker","Option:Hide", "Option:Lag Switch","Option:Close"]
selected_index = 1  
is_active = False 

def get_cpu_usage():
    return psutil.cpu_percent()

def get_ram_usage():
    return psutil.virtual_memory().percent

def get_memory_usage():
    global selected_index
    return options[selected_index]

def update_metrics(cpu_value, ram_value,memory_value, status_label):
    cpu_usage = get_cpu_usage()
    ram_usage = get_ram_usage()
    memory_usage = get_memory_usage()
    
    cpu_value.config(text=f"{cpu_usage:.1f}%")
    ram_value.config(text=f"{ram_usage:.1f}%")
    memory_value.config(text=f"{memory_usage}")

    status_label.config(text="Activate" if is_active else "Inactive")

    header_window.after(500,update_metrics, cpu_value, ram_value, memory_value,status_label)

def on_press(event):
    global x_start, y_start, window_x, window_y
    x_start = event.x_root
    y_start = event.y_root
    window_x = header_window.winfo_x()
    window_y = header_window.winfo_y()

def on_drag(event):
    x = event.x_root - x_start
    y = event.y_root - y_start
    header_window.geometry(f'+{window_x + x}+{window_y + y}')
    content_window.geometry(f'+{window_x + x}+{window_y + y + 30}')

def switch_option(keyboard_event):
    global selected_index, is_active
    # print(f"Key pressed: {keyboard_event.name}")
    if keyboard_event.name == 'up':
        selected_index = (selected_index - 1) % len(options)
    elif keyboard_event.name == 'down':
        selected_index = (selected_index + 1) % len(options)
    
    is_active = False
    memory_label.config(text=get_memory_usage())
    status_label.config(text="Inactive")

def toggle_activation(keyboard_event):
    global is_active
    if keyboard_event.name == 'right':
        if not is_active:
            is_active = True
            start_option_function()
    elif keyboard_event.name == 'left':
        if is_active:
            is_active = False
            stop_option_function()
    
    status_label.config(text="Activate" if is_active else "Inactive")

def auto_clicker_function():
    # print("Auto clicker started")
    while is_active and selected_index == 0:
        try:
            mouse = Controller()
            mouse.click(Button.left,1)
            time.sleep(.07)
        except:
            break

def hide_function():
    header_window.wm_attributes('-alpha', 0.0)
    content_window.wm_attributes('-alpha', 0.0)

def lag_switch_function():
    try:
        # print("Activating lag switch")
        subprocess.run(['netsh', 'advfirewall', 'firewall', 'add', 'rule', 'name=BlockOutLagSwitch', 'dir=out', 'action=block', 'protocol=any', 'enable=yes'], check=True)
    except:
        pass

def close_function():
    try:
        subprocess.run(['netsh', 'advfirewall', 'firewall', 'delete', 'rule', 'name=BlockOutLagSwitch'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"No Rule!")
    os._exit(0)

def start_option_function():
    global thread
    if selected_index == 0:
        thread = threading.Thread(target=auto_clicker_function, daemon=True)
    elif selected_index == 1:
        thread = threading.Thread(target=hide_function, daemon=True)
    elif selected_index == 2:
        thread = threading.Thread(target=lag_switch_function, daemon=True)
    elif selected_index == 3:
        thread = threading.Thread(target=close_function, daemon=True)
    
    thread.start()

def stop_option_function():
    global thread
    header_window.wm_attributes('-alpha', 1.0)
    content_window.wm_attributes('-alpha', 0.9)
    try:
        subprocess.run(['netsh', 'advfirewall', 'firewall', 'delete', 'rule', 'name=BlockOutLagSwitch'], check=True)
        print("Deleted rule!")
    except subprocess.CalledProcessError as e:
        print("No Rule!")
    if thread and thread.is_alive():
        is_active = False
        thread.join(timeout=1)


def create_window():
    global header_window, content_window, thread, root, memory_label, status_label
    root = tk.Tk()
    root.withdraw() 

    window_width = 220
    window_height = 130
    header_height = 30
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    x_position = screen_width - window_width - 5
    y_position = 70

    header_window = tk.Toplevel()
    header_window.geometry(f"{window_width}x{header_height}+{x_position}+{y_position}")
    header_window.overrideredirect(True)
    header_window.wm_attributes('-alpha',1.0)  
    header_window.wm_attributes('-topmost',1)  


    content_window = tk.Toplevel()
    content_window.geometry(f"{window_width}x{window_height - header_height}+{x_position}+{y_position + header_height}")
    content_window.overrideredirect(True)
    content_window.wm_attributes('-alpha',0.9) 
    content_window.wm_attributes('-topmost', 1)  


    header_frame = tk.Frame(header_window, height=header_height, bg="#191e32")
    header_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    content_frame = tk.Frame(content_window, height=window_height - header_height, bg="#262d45")
    content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    header_label = tk.Label(header_frame, bg="#191e32", fg="white", font=("Arial", 12), text="SYSTEM")
    header_label.pack(side=tk.TOP, pady=5)

    labels = ["CPU                           ", "RAM                           "]
    values = ["0%", "0%"]
    
    for i, label in enumerate(labels):
        tk.Label(content_frame, bg="#262d45", fg="white", font=("Arial", 10), text=label).grid(row=i, column=0, padx=8, pady=5, sticky="w")
        tk.Label(content_frame, bg="#262d45", fg="white", font=("Arial", 10), text=values[i]).grid(row=i, column=1, padx=15, pady=5, sticky="e")
    
    memory_label = tk.Label(content_frame, bg="#262d45", fg="white", font=("Arial", 10), text=options[selected_index])
    memory_label.grid(row=2, column=0, padx=8, pady=5, sticky="w")

    status_label = tk.Label(content_frame, bg="#262d45", fg="white", font=("Arial", 9), text="Inactive")
    status_label.grid(row=2, column=1, padx=(0, 16), pady=5, sticky="e")  

    cpu_label = content_frame.grid_slaves(row=0, column=1)[0]
    ram_label = content_frame.grid_slaves(row=1, column=1)[0]

    header_window.bind('<ButtonPress-1>', on_press)
    header_window.bind('<B1-Motion>', on_drag)

    keyboard.on_press_key('up', switch_option)
    keyboard.on_press_key('down', switch_option)
    keyboard.on_press_key('right', toggle_activation)
    keyboard.on_press_key('left', toggle_activation)

    header_window.lift()
    content_window.lift()

    update_metrics(cpu_label, ram_label, memory_label, status_label)

    root.mainloop()

create_window()
