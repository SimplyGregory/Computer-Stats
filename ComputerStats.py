import tkinter as tk
from datetime import datetime

try:
    import psutil
except Exception:
    psutil = None

try:
    import keyboard as global_keyboard
except Exception:
    global_keyboard = None


OPTIONS = ["Option:Hide", "Option:Close"]


class WindowPair:
    def __init__(
        self,
        *,
        root: tk.Tk,
        x: int,
        y: int,
        width: int,
        height: int,
        header_height: int,
        header_alpha: float,
        content_alpha: float,
        header_bg: str,
        content_bg: str,
        topmost: bool,
    ):
        self._root = root
        self._width = width
        self._height = height
        self._header_height = header_height

        self._x_start = 0
        self._y_start = 0
        self._window_x = 0
        self._window_y = 0

        self.header_window = tk.Toplevel(root)
        self.header_window.geometry(f"{width}x{header_height}+{x}+{y}")
        self.header_window.overrideredirect(True)
        self.header_window.wm_attributes("-alpha", float(header_alpha))
        if topmost:
            self.header_window.wm_attributes("-topmost", 1)

        self.content_window = tk.Toplevel(root)
        self.content_window.geometry(f"{width}x{height - header_height}+{x}+{y + header_height}")
        self.content_window.overrideredirect(True)
        self.content_window.wm_attributes("-alpha", float(content_alpha))
        if topmost:
            self.content_window.wm_attributes("-topmost", 1)

        self.header_frame = tk.Frame(self.header_window, height=header_height, bg=header_bg)
        self.header_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.content_frame = tk.Frame(self.content_window, height=height - header_height, bg=content_bg)
        self.content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.header_window.bind("<ButtonPress-1>", self._on_press)
        self.header_window.bind("<B1-Motion>", self._on_drag)
        self.header_window.bind("<ButtonPress-1>", self._focus_on_click, add=True)
        self.content_window.bind("<ButtonPress-1>", self._focus_on_click, add=True)

        self.header_window.lift()
        self.content_window.lift()

    def _focus_on_click(self, _event):
        try:
            self.header_window.focus_force()
        except Exception:
            pass

    def enforce_topmost(self):
        try:
            self.header_window.wm_attributes("-topmost", 1)
            self.content_window.wm_attributes("-topmost", 1)
            self.header_window.lift()
            self.content_window.lift()
        except Exception:
            pass

    def _on_press(self, event):
        self._x_start = event.x_root
        self._y_start = event.y_root
        self._window_x = self.header_window.winfo_x()
        self._window_y = self.header_window.winfo_y()

    def _on_drag(self, event):
        dx = event.x_root - self._x_start
        dy = event.y_root - self._y_start

        new_x = self._window_x + dx
        new_y = self._window_y + dy

        self.header_window.geometry(f"+{new_x}+{new_y}")
        self.content_window.geometry(f"+{new_x}+{new_y + self._header_height}")


def _get_cpu_percent() -> float:
    if psutil is None:
        return 0.0
    return float(psutil.cpu_percent())


def _get_ram_percent() -> float:
    if psutil is None:
        return 0.0
    return float(psutil.virtual_memory().percent)


def main():
    root = tk.Tk()
    root.withdraw()

    screen_width = root.winfo_screenwidth()

    width = 220

    clock_height = 60
    stats_height = 130
    header_height = 30

    x = screen_width - width - 5

    clock_pair = WindowPair(
        root=root,
        x=x,
        y=5,
        width=width,
        height=clock_height,
        header_height=header_height,
        header_alpha=1.0,
        content_alpha=0.9,
        header_bg="#191e32",
        content_bg="#262d45",
        topmost=True,
    )

    time_label = tk.Label(clock_pair.header_frame, bg="#191e32", fg="white", font=("Arial", 12))
    time_label.pack(side=tk.TOP, pady=5)

    day_label = tk.Label(clock_pair.content_frame, bg="#262d45", fg="white", font=("Arial", 10))
    day_label.pack(side=tk.LEFT, padx=5)

    date_label = tk.Label(clock_pair.content_frame, bg="#262d45", fg="white", font=("Arial", 10))
    date_label.pack(side=tk.RIGHT, padx=5)

    stats_pair = WindowPair(
        root=root,
        x=x,
        y=70,
        width=width,
        height=stats_height,
        header_height=header_height,
        header_alpha=1.0,
        content_alpha=0.9,
        header_bg="#191e32",
        content_bg="#262d45",
        topmost=True,
    )

    header_label = tk.Label(stats_pair.header_frame, bg="#191e32", fg="white", font=("Arial", 12), text="SYSTEM")
    header_label.pack(side=tk.TOP, pady=5)

    cpu_name = tk.Label(stats_pair.content_frame, bg="#262d45", fg="white", font=("Arial", 10), text="CPU")
    cpu_value = tk.Label(stats_pair.content_frame, bg="#262d45", fg="white", font=("Arial", 10), text="0%")
    ram_name = tk.Label(stats_pair.content_frame, bg="#262d45", fg="white", font=("Arial", 10), text="RAM")
    ram_value = tk.Label(stats_pair.content_frame, bg="#262d45", fg="white", font=("Arial", 10), text="0%")

    tool_label = tk.Label(stats_pair.content_frame, bg="#262d45", fg="white", font=("Arial", 10), text=OPTIONS[0])
    status_label = tk.Label(stats_pair.content_frame, bg="#262d45", fg="white", font=("Arial", 9), text="Inactive")

    cpu_name.grid(row=0, column=0, padx=8, pady=5, sticky="w")
    cpu_value.grid(row=0, column=1, padx=15, pady=5, sticky="e")
    ram_name.grid(row=1, column=0, padx=8, pady=5, sticky="w")
    ram_value.grid(row=1, column=1, padx=15, pady=5, sticky="e")

    tool_label.grid(row=2, column=0, padx=8, pady=5, sticky="w")
    status_label.grid(row=2, column=1, padx=(0, 16), pady=5, sticky="e")

    psutil_label = None
    if psutil is None:
        psutil_label = tk.Label(
            stats_pair.content_frame,
            bg="#262d45",
            fg="#ffcc00",
            font=("Arial", 8),
            text="psutil not installed",
        )
        psutil_label.grid(row=3, column=0, columnspan=2, padx=8, pady=(2, 6), sticky="w")

    selected_index = 0
    is_active = False

    def cleanup_and_quit():
        if global_keyboard is not None:
            try:
                global_keyboard.unhook_all()
            except Exception:
                pass
        root.quit()

    def set_visibility(visible: bool):
        try:
            if visible:
                clock_pair.header_window.wm_attributes("-alpha", 1.0)
                clock_pair.content_window.wm_attributes("-alpha", 0.9)
                stats_pair.header_window.wm_attributes("-alpha", 1.0)
                stats_pair.content_window.wm_attributes("-alpha", 0.9)
            else:
                clock_pair.header_window.wm_attributes("-alpha", 0.0)
                clock_pair.content_window.wm_attributes("-alpha", 0.0)
                stats_pair.header_window.wm_attributes("-alpha", 0.0)
                stats_pair.content_window.wm_attributes("-alpha", 0.0)
        except Exception:
            pass

    def update_tool_ui():
        tool_label.config(text=OPTIONS[selected_index])
        status_label.config(text="Activate" if is_active else "Inactive")

    def stop_tool():
        nonlocal is_active
        is_active = False
        set_visibility(True)
        update_tool_ui()

    def start_tool():
        nonlocal is_active
        is_active = True
        if selected_index == 0:
            set_visibility(False)
        elif selected_index == 1:
            root.after(50, cleanup_and_quit)
        update_tool_ui()

    def on_up(_event=None):
        nonlocal selected_index
        selected_index = (selected_index - 1) % len(OPTIONS)
        stop_tool()
        tool_label.config(text=OPTIONS[selected_index])

    def on_down(_event=None):
        nonlocal selected_index
        selected_index = (selected_index + 1) % len(OPTIONS)
        stop_tool()
        tool_label.config(text=OPTIONS[selected_index])

    def on_right(_event=None):
        if not is_active:
            start_tool()

    def on_left(_event=None):
        if is_active:
            stop_tool()

    for w in (stats_pair.header_window, stats_pair.content_window):
        w.bind("<Up>", on_up)
        w.bind("<Down>", on_down)
        w.bind("<Right>", on_right)
        w.bind("<Left>", on_left)

    def bind_global_hotkeys():
        if global_keyboard is None:
            return

        def _safe_call(fn):
            try:
                root.after(0, fn)
            except Exception:
                pass

        global_keyboard.on_press_key("up", lambda _e: _safe_call(on_up))
        global_keyboard.on_press_key("down", lambda _e: _safe_call(on_down))
        global_keyboard.on_press_key("right", lambda _e: _safe_call(on_right))
        global_keyboard.on_press_key("left", lambda _e: _safe_call(on_left))

    bind_global_hotkeys()

    def enforce_always_on_top():
        clock_pair.enforce_topmost()
        stats_pair.enforce_topmost()
        root.after(2000, enforce_always_on_top)

    enforce_always_on_top()

    def update_clock():
        now = datetime.now()
        time_label.config(text=now.strftime("%I:%M %p"))
        day_label.config(text=now.strftime("%A"))
        date_label.config(text=now.strftime("%d.%m.%Y"))
        root.after(1000, update_clock)

    def update_stats():
        cpu_value.config(text=f"{_get_cpu_percent():.1f}%")
        ram_value.config(text=f"{_get_ram_percent():.1f}%")
        update_tool_ui()
        root.after(500, update_stats)

    update_clock()
    update_stats()

    root.mainloop()


if __name__ == "__main__":
    main()
