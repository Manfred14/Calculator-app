import tkinter as tk
import math
import sys
import os

root = tk.Tk()
root.title("Calculator")
root.geometry("420x600")

# ===========================
# THEMES
# ===========================
LIGHT_THEME = {
    "bg": "#ffffff",
    "fg": "#000000",
    "button_bg": "#e6e6e6",
    "button_fg": "#000000",
    "special_bg": "#d4d4d4"
}

DARK_THEME = {
    "bg": "#1e1e1e",
    "fg": "#ffffff",
    "button_bg": "#333333",
    "button_fg": "#ffffff",
    "special_bg": "#444444"
}

current_theme = LIGHT_THEME

expression = ""
memory = 0.0
history = []

# ===========================
# THEME FUNCTIONS
# ===========================
def apply_theme(theme):
    root.config(bg=theme["bg"])
    entry.config(bg=theme["bg"], fg=theme["fg"])

    for button in buttons_list:
        button.config(bg=theme["button_bg"], fg=theme["button_fg"])

    for button in special_buttons:
        button.config(bg=theme["special_bg"], fg=theme["button_fg"])


def toggle_theme():
    global current_theme
    current_theme = DARK_THEME if current_theme == LIGHT_THEME else LIGHT_THEME
    apply_theme(current_theme)

# ===========================
# ENTRY FIELD
# ===========================
entry = tk.Entry(root, width=18, font=("Arial", 30), justify="right")
entry.pack(pady=20)

# ===========================
# CALCULATOR FUNCTIONS
# ===========================
def press(val):
    global expression

    # --- Instant Trig Functions (Degrees) ---
    if val == "sin":
        try:
            num = float(expression)
            result = math.sin(math.radians(num))
            expression = str(result)
            entry.delete(0, tk.END)
            entry.insert(tk.END, expression)
        except:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")
            expression = ""
        return

    if val == "cos":
        try:
            num = float(expression)
            result = math.cos(math.radians(num))
            expression = str(result)
            entry.delete(0, tk.END)
            entry.insert(tk.END, expression)
        except:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")
            expression = ""
        return

    if val == "tan":
        try:
            num = float(expression)
            result = math.tan(math.radians(num))
            expression = str(result)
            entry.delete(0, tk.END)
            entry.insert(tk.END, expression)
        except:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")
            expression = ""
        return

    # Normal button input
    expression += str(val)
    entry.delete(0, tk.END)
    entry.insert(tk.END, expression)

def backspace():
    """Remove last character"""
    global expression
    expression = expression[:-1]
    entry.delete(0, tk.END)
    entry.insert(tk.END, expression)

def clear():
    global expression
    expression = ""
    entry.delete(0, tk.END)

def equal():
    global expression
    try:
        result = str(eval(expression))
        history.append(f"{expression} = {result}")
        entry.delete(0, tk.END)
        entry.insert(tk.END, result)
        expression = result
    except Exception:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")
        expression = ""

def show_history():
    hist_window = tk.Toplevel(root)
    hist_window.title("Calculation History")
    hist_window.geometry("300x400")

    for item in history:
        tk.Label(hist_window, text=item, font=("Arial", 12)).pack()

# ===========================
# MEMORY FUNCTIONS
# ===========================
def memory_add():
    global memory, expression
    try:
        memory += float(expression)
    except:
        pass

def memory_sub():
    global memory, expression
    try:
        memory -= float(expression)
    except:
        pass

def memory_recall():
    global expression
    entry.delete(0, tk.END)
    entry.insert(tk.END, str(memory))
    expression = str(memory)

def memory_clear():
    global memory
    memory = 0.0

# ===========================
# BUTTONS
# ===========================
buttons = [
    ["7", "8", "9", "/", "sin"],
    ["4", "5", "6", "*", "cos"],
    ["1", "2", "3", "-", "tan"],
    ["0", ".", "(", ")", "+"],
]

buttons_list = []
special_buttons = []

for row in buttons:
    frame = tk.Frame(root)
    frame.pack()
    for b in row:
        btn = tk.Button(frame, text=b, width=5, height=2, font=("Arial", 16),
                        command=lambda x=b: press(x))
        btn.pack(side="left", padx=3, pady=3)
        buttons_list.append(btn)

# Special Buttons Row
special_frame = tk.Frame(root)
special_frame.pack(pady=10)

btn_equal = tk.Button(special_frame, text="=", width=5, height=2, font=("Arial", 16), command=equal)
btn_equal.pack(side="left", padx=5)
special_buttons.append(btn_equal)

btn_clear = tk.Button(special_frame, text="C", width=5, height=2, font=("Arial", 16), command=clear)
btn_clear.pack(side="left", padx=5)
special_buttons.append(btn_clear)

btn_back = tk.Button(special_frame, text="⌫", width=5, height=2, font=("Arial", 16), command=backspace)
btn_back.pack(side="left", padx=5)
special_buttons.append(btn_back)

btn_sqrt = tk.Button(special_frame, text="√", width=5, height=2, font=("Arial", 16),
                     command=lambda: press("math.sqrt("))
btn_sqrt.pack(side="left", padx=5)
special_buttons.append(btn_sqrt)

btn_pow = tk.Button(special_frame, text="x²", width=5, height=2, font=("Arial", 16),
                    command=lambda: press("**2"))
btn_pow.pack(side="left", padx=5)
special_buttons.append(btn_pow)

# Memory Buttons
memory_frame = tk.Frame(root)
memory_frame.pack(pady=10)

memory_buttons = {
    "M+": memory_add,
    "M-": memory_sub,
    "MR": memory_recall,
    "MC": memory_clear
}

for label, func in memory_buttons.items():
    b = tk.Button(memory_frame, text=label, width=5, height=2, font=("Arial", 16), command=func)
    b.pack(side="left", padx=5)
    special_buttons.append(b)

# History Button
history_btn = tk.Button(root, text="History", width=10, height=2, font=("Arial", 16), command=show_history)
history_btn.pack(pady=10)
special_buttons.append(history_btn)

# Theme Button
theme_btn = tk.Button(root, text="Toggle Theme", width=12, height=2, font=("Arial", 16), command=toggle_theme)
theme_btn.pack(pady=10)
special_buttons.append(theme_btn)

# Apply initial theme
apply_theme(current_theme)

# ===========================
# ICON (PyInstaller Safe)
# ===========================
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

icon_path = os.path.join(base_path, "calculator.ico")
root.iconbitmap(icon_path)

root.mainloop()
