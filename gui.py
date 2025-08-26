import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import PhotoImage
import latchck
import threading
import os
from PIL import Image, ImageTk

# --- Tooltip Helper ---
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)
    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, _, cy = self.widget.bbox("insert") if hasattr(self.widget, 'bbox') else (0,0,0,0)
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left', background="#ffffe0", relief='solid', borderwidth=1, font=(None, 9))
        label.pack(ipadx=4)
    def hide_tip(self, event=None):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

# --- GUI Setup ---
root = tk.Tk()
root.title("Simple Enhancer")
root.geometry("500x340")
root.resizable(False, False)
root.configure(bg="#f7f9fa")  # Subtle background

# --- Logo & Title ---
logo_frame = tk.Frame(root, bg="#f7f9fa")
logo_frame.pack(pady=(10, 0))

logo_img = None
logo_path = os.path.join(os.path.dirname(__file__), 'enhance.png')
try:
    from PIL import Image, ImageTk
    img = Image.open(logo_path)
    img.thumbnail((48, 48))
    logo_img = ImageTk.PhotoImage(img)
    logo_label = tk.Label(logo_frame, image=logo_img, bg="#f7f9fa")
    logo_label.pack(side='left', padx=(0, 10))
except Exception:
    logo_label = tk.Label(logo_frame, text="🦾", font=("Arial", 28), bg="#f7f9fa")
    logo_label.pack(side='left', padx=(0, 10))

title_label = tk.Label(logo_frame, text="Simple Enhancer", font=("Segoe UI", 20, "bold"), bg="#f7f9fa", fg="#2d415a")
title_label.pack(side='left')

# --- Main Frame ---
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill='both', expand=True, pady=(5,0))

# --- Theme Toggle ---
theme_frame = ttk.LabelFrame(main_frame, text="Theme")
theme_frame.grid(row=0, column=0, columnspan=3, pady=(0,10), sticky='w')

current_theme = tk.StringVar(value='Light')
light_rb = ttk.Radiobutton(theme_frame, text='Light', value='Light', variable=current_theme,
                            command=lambda: set_theme(current_theme.get()))
light_rb.pack(side='left', padx=5, pady=5)
dark_rb = ttk.Radiobutton(theme_frame, text='Dark', value='Dark', variable=current_theme,
                           command=lambda: set_theme(current_theme.get()))
dark_rb.pack(side='left', padx=5, pady=5)
ToolTip(light_rb, "Use light mode")
ToolTip(dark_rb, "Use dark mode")

# --- Separator ---
sep1 = ttk.Separator(main_frame, orient='horizontal')
sep1.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(5, 10))

# --- Window Title Selection ---
ttk.Label(main_frame, text="Window Title:").grid(row=2, column=0, sticky='w', pady=3)
window_path_var = tk.StringVar()
window_entry = ttk.Entry(main_frame, textvariable=window_path_var, width=40)
window_entry.insert(0, "Calculator")
window_entry.grid(row=2, column=1, padx=5, pady=3)
ToolTip(window_entry, "Enter the title of the window to enhance (e.g., Calculator)")

# --- ONNX Model Selection ---
ttk.Label(main_frame, text="ONNX Model:").grid(row=3, column=0, sticky='w', pady=3)
model_path_var = tk.StringVar()
model_entry = ttk.Entry(main_frame, textvariable=model_path_var, width=40)
model_entry.grid(row=3, column=1, padx=5, pady=3)
ToolTip(model_entry, "Path to your ONNX model file")

def browse_model():
    path = filedialog.askopenfilename(title="Select ONNX Model",
                                      filetypes=[("ONNX files", "*.onnx"), ("All files", "*")])
    if path:
        model_path_var.set(path)

browse_model_btn = ttk.Button(main_frame, text="Browse", command=browse_model)
browse_model_btn.grid(row=3, column=2, padx=5)
ToolTip(browse_model_btn, "Browse for ONNX model file")

# --- Separator ---
sep2 = ttk.Separator(main_frame, orient='horizontal')
sep2.grid(row=4, column=0, columnspan=3, sticky='ew', pady=(10, 10))

# --- Run Button ---
def on_enter(e):
    e.widget.configure(style='Accent.TButton')
def on_leave(e):
    e.widget.configure(style='TButton')

def run_script():
    window_title = window_path_var.get().strip()
    model_path = model_path_var.get().strip()
    if not window_title:
        status_label.config(text="Please enter a window title.")
        return
    if not model_path:
        status_label.config(text="Please select an ONNX model.")
        return
    def worker():
        try:
            start_btn.config(state='disabled')
            progress.start()
            status_label.config(text="Enhancing...")
            latchck.start_capture(window_title, model_path)
            status_label.config(text="Done!")
        except Exception as e:
            status_label.config(text=f"Error: {e}")
        finally:
            progress.stop()
            start_btn.config(state='normal')
    threading.Thread(target=worker, daemon=True).start()

start_btn = ttk.Button(main_frame, text="Start", command=run_script)
start_btn.grid(row=5, column=0, columnspan=3, pady=10)
ToolTip(start_btn, "Start the enhancement process")
start_btn.bind("<Enter>", on_enter)
start_btn.bind("<Leave>", on_leave)

# --- Status & Progress ---
status_label = ttk.Label(main_frame, text="Ready")
status_label.grid(row=6, column=0, columnspan=3, pady=(10,0), sticky='w')

progress = ttk.Progressbar(main_frame, mode='indeterminate', length=400, style='Custom.Horizontal.TProgressbar')
progress.grid(row=7, column=0, columnspan=3, sticky='ew', pady=5)

# --- Progressbar Style ---
style = ttk.Style()
# Available themes: 'clam', 'alt', 'default', 'classic'
def set_theme(mode):
    if mode == 'Dark':
        style.theme_use('clam')
        style.configure('.', background='#333333', foreground='#ffffff')
        style.configure('TButton', background='#555555', foreground='#ffffff')
        style.configure('Accent.TButton', background='#6a8caf', foreground='#ffffff')
        style.configure('TEntry', fieldbackground='#555555', foreground='#ffffff')
        style.configure('TLabel', background='#333333', foreground='#ffffff')
        style.configure('Custom.Horizontal.TProgressbar', troughcolor='#222', background='#6a8caf', bordercolor='#222')
    else:
        style.theme_use('default')
        style.configure('.', background='#f0f0f0', foreground='#000000')
        style.configure('TButton', background='#e0e0e0', foreground='#000000')
        style.configure('Accent.TButton', background='#6a8caf', foreground='#ffffff')
        style.configure('TEntry', fieldbackground='#ffffff', foreground='#000000')
        style.configure('TLabel', background='#f0f0f0', foreground='#000000')
        style.configure('Custom.Horizontal.TProgressbar', troughcolor='#dbeafe', background='#6a8caf', bordercolor='#dbeafe')

# Initialize theme
set_theme(current_theme.get())

# --- Footer / Credits ---
footer = tk.Label(root, text="© 2024 Simple Enhancer | Powered by Tkinter", font=("Segoe UI", 9), bg="#f7f9fa", fg="#7a8ca3")
footer.pack(side='bottom', pady=(0, 5))

root.mainloop()
