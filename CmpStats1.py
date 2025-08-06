import tkinter as tk
from datetime import datetime

def update_time_labels(time_label,day_label, date_label):
    try:
        now = datetime.now()
        time_str = now.strftime("%I:%M %p") 
        day_str = now.strftime("%A")
        date_str = now.strftime("%d.%m.%Y")
        
        time_label.config(text=time_str)
        day_label.config(text=day_str)
        date_label.config(text=date_str)
        # print(f"Time updated: {time_str}")
        
        time_label.after(1000,update_time_labels, time_label, day_label,date_label)
    except:
        pass

def on_press(event):
    global x_start, y_start, window_x, window_y
    # print("Mouse press detected")
    x_start = event.x_root
    y_start = event.y_root
    window_x = header_window.winfo_x()
    window_y = header_window.winfo_y()

def on_drag(event):
    x = event.x_root - x_start
    y = event.y_root - y_start
    header_window.geometry(f'+{window_x + x}+{window_y + y}')
    content_window.geometry(f'+{window_x + x}+{window_y + y + 30}')

def create_window():
    global header_window, content_window
    root = tk.Tk()
    root.withdraw() 

    window_width = 220
    window_height = 60
    header_height = 30
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    x_position = screen_width - window_width - 5
    y_position = 5

    header_window = tk.Toplevel()
    header_window.geometry(f"{window_width}x{header_height}+{x_position}+{y_position}")
    header_window.overrideredirect(True)
    header_window.wm_attributes('-alpha', 1.0) 
    
    content_window = tk.Toplevel()
    content_window.geometry(f"{window_width}x{window_height - header_height}+{x_position}+{y_position + header_height}")
    content_window.overrideredirect(True)
    content_window.wm_attributes('-alpha', 0.9)

    header_frame = tk.Frame(header_window,height=header_height, bg="#191e32")
    header_frame.pack(side=tk.TOP,fill=tk.BOTH, expand=True)

    content_frame = tk.Frame(content_window,height=window_height - header_height, bg="#262d45")
    content_frame.pack(side=tk.TOP, fill=tk.BOTH,expand=True)

    time_label = tk.Label(header_frame, bg="#191e32",fg="white", font=("Arial", 12))
    time_label.pack(side=tk.TOP,pady=5)

    day_label = tk.Label(content_frame, bg="#262d45", fg="white", font=("Arial", 10))
    day_label.pack(side=tk.LEFT, padx=5)

    date_label = tk.Label(content_frame, bg="#262d45", fg="white", font=("Arial", 10))
    date_label.pack(side=tk.RIGHT, padx=5)

    time_label.pack(side=tk.TOP, fill=tk.X, padx=10)

    header_window.bind('<ButtonPress-1>', on_press)
    header_window.bind('<B1-Motion>', on_drag)

    header_window.lift()
    content_window.lift()

    update_time_labels(time_label, day_label, date_label)

    root.mainloop()

create_window()
